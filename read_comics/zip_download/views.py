import math
from typing import Any
from zipfile import ZIP_DEFLATED

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from zip_download.zip_downloader import ZipDownloader


class BaseZipDownloadView(LoginRequiredMixin, View):
    sublist_querysets = None
    base_model = None
    base_slug_kwarg = "slug"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.obj = None

    @staticmethod
    def escape_file_name(filename):
        return filename.replace("/", " - ").replace(":", " - ").replace("\t", " ").replace("\n", " ")

    def get_issues_queryset(self):
        return self.sublist_querysets.get_issues_queryset(self.obj)

    def get_base_object(self):
        return get_object_or_404(self.base_model, slug=self.kwargs.get(self.base_slug_kwarg))

    def get_grouped_filename(self, issue):
        filename = ""
        if issue.volume:
            filename = f"{self.escape_file_name(issue.volume.name)} ({issue.volume.start_year})" \
                       f"/{self.escape_file_name(issue.volume.name)} #" + filename
            if issue.volume.publisher:
                filename = f"{self.escape_file_name(str(issue.volume.publisher))}/" + filename
            else:
                filename = "Unknown publisher/" + filename
        else:
            filename = "Unknown volume/Unknown volume #"

        filename += issue.number

        if issue.name:
            filename += f" {self.escape_file_name(issue.name)}"

        filename += issue.space_key[-4:]

        return filename

    def get_grouped_files(self):
        self.obj = self.get_base_object()
        q = self.get_issues_queryset()

        return [
            (
                self.get_grouped_filename(x),
                x.download_link
            )
            for x in q
        ]

    def get_ordered_files(self):
        self.obj = self.get_base_object()
        q = self.get_issues_queryset().order_by(
            "cover_date", "volume__name", "volume__start_year", "numerical_number", "number"
        )
        issues_count = q.count()

        if issues_count:
            num_length = math.ceil(math.log10(q.count()))

            return [
                (
                    self.escape_file_name(
                        f"{str(num).rjust(num_length, '0')} - {x.volume.name} #{x.number} {x.name or ''}".rstrip(" ")
                        + x.space_key[-4:]
                    ),
                    x.download_link
                )
                for num, x in enumerate(q, 1)
            ]
        else:
            return []

    def get_zip_name(self):
        return self.escape_file_name(str(self.obj))

    def get(self, request, *args, **kwargs):
        ordering = self.request.GET.get("names")
        if ordering == "ordered":
            files = self.get_ordered_files()
        else:
            files = self.get_grouped_files()
        zip_name = self.get_zip_name()

        z = ZipDownloader(compression=ZIP_DEFLATED, allowZip64=True, request=request)
        z.write_links(files)

        response = StreamingHttpResponse(z, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_name}.zip"'

        return response
