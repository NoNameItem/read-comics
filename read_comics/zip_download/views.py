from zipfile import ZIP_DEFLATED

from django.http import StreamingHttpResponse
from django.views import View
from zip_download.zip_downloader import ZipDownloader


class BaseZipDownloadView(View):
    @staticmethod
    def escape_file_name(filename):
        return filename.replace("/", ' - ').replace(":", ' - ')

    def get_files(self):
        raise NotImplementedError('subclasses of BaseZipDownloadView must provide a get_files() method')

    def get_zip_name(self):
        raise NotImplementedError('subclasses of BaseZipDownloadView must provide a get_zip_name() method')

    def get(self, request, *args, **kwargs):
        files = self.get_files()
        zip_name = self.get_zip_name()

        z = ZipDownloader(compression=ZIP_DEFLATED, allowZip64=True)
        z.write_links(files)

        response = StreamingHttpResponse(z, content_type="application/zip")
        response['Content-Disposition'] = "attachment; filename=\"{0}.zip\"".format(zip_name)

        return response
