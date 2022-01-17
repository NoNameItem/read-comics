from typing import Any
from zipfile import ZIP_DEFLATED

from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from zip_download.zip_downloader import ZipDownloader


class BaseZipDownloadView(View):
    sublist_querysets = None
    base_model = None
    base_slug_kwarg = "slug"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.obj = None

    @staticmethod
    def escape_file_name(filename):
        return filename.replace("/", ' - ').replace(":", ' - ').replace('\t', ' ').replace('\n', ' ')

    def get_issues_queryset(self):
        return self.sublist_querysets.get_issues_queryset(self.obj)

    def get_base_object(self):
        return get_object_or_404(self.base_model, slug=self.kwargs.get(self.base_slug_kwarg))

    def get_filename(self, issue):
        filename = ""
        if issue.volume:
            filename = f"{self.escape_file_name(issue.volume.name)} ({issue.volume.start_year})" \
                       f"/{self.escape_file_name(issue.volume.name)} #" + filename
            if issue.volume.publisher:
                filename = f"{self.escape_file_name(str(issue.volume.publisher))}/" + filename
            else:
                filename = "Unknown publisher/" + filename
        else:
            filename = 'Unknown volume/Unknown volume #'

        filename += issue.number

        if issue.name:
            filename += f" {self.escape_file_name(issue.name)}"

        filename += issue.space_key[-4:]

        return filename

    def get_files(self):
        self.obj = self.get_base_object()
        q = self.get_issues_queryset()

        files = [
            (
                self.get_filename(x),
                x.download_link
            )
            for x in q
        ]

        return files

    def get_zip_name(self):
        return self.escape_file_name(str(self.obj))

    def get(self, request, *args, **kwargs):
        files = self.get_files()
        zip_name = self.get_zip_name()

        z = ZipDownloader(compression=ZIP_DEFLATED, allowZip64=True)
        z.write_links(files)

        response = StreamingHttpResponse(z, content_type="application/zip")
        response['Content-Disposition'] = "attachment; filename=\"{0}.zip\"".format(zip_name)

        return response
