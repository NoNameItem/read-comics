import io
from zipfile import ZIP_STORED

import gevent.pool
import requests
import zipstream


class Downloader:
    def __init__(self, links):
        self.links = links

    def download_file(self, link):
        # print("Start download " + link[1])
        r = requests.get(link[1])
        f = io.BytesIO(r.content)
        # print("Downloaded " + link[1])
        return link[0], f

    def __iter__(self):
        pool = gevent.pool.Pool(1)
        for file in pool.imap_unordered(self.download_file, self.links, maxsize=2):
            # print("Yielded: " + file[0])
            yield file[0], file[1]


class ZipDownloader(zipstream.ZipFile):
    def __init__(self, fileobj=None, mode='w', compression=ZIP_STORED, allowZip64=False):
        super().__init__(fileobj, mode, compression, allowZip64)
        self.links = []
        self.links_compress_type = None
        self.links_buffersize = None

    def write_links(self, links, compress_type=None, buffer_size=None):
        self.links += links
        self.links_compress_type = compress_type
        self.links_buffersize = buffer_size

    def flush(self):
        try:
            while self.paths_to_write:
                kwargs = self.paths_to_write.pop()
                for data in self.__write(**kwargs):
                    yield data
            if self.links:
                downloader = Downloader(self.links)
                for file in downloader:
                    for data in self._ZipFile__write(arcname=file[0], iterable=file[1],
                                                     buffer_size=self.links_buffersize,
                                                     compress_type=self.links_compress_type):
                        yield data
        except Exception as e:
            print(e)
            raise


# class FileWrapper:
#     """
#     Get S3 key and wraps it to iterator.
#
#     Class needed for downloading multiple issues and to postpone download of actual file until zip started
#     """
#
#     def __init__(self, url):
#         self.url = url
#         self.file = None
#
#     def get_file(self):
#         r = requests.get(self.url)
#         self.file = io.BytesIO(r.content)
#         self.file.seek(0)
#         yield self.file.read()
