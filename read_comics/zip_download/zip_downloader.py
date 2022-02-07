import tempfile
from zipfile import ZIP_DEFLATED

import gevent.pool
import requests
import zipstream
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Downloader:
    def __init__(self, links):
        self.links = links

    def download_file(self, link):
        # print("Start download " + link[1])
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        r = http.get(link[1])
        fp = tempfile.TemporaryFile()
        fp.write(r.content)
        fp.seek(0)
        # f = io.BytesIO(r.content)
        # print("Downloaded " + link[1])
        return link[0], fp

    def __iter__(self):
        pool = gevent.pool.Pool(5)
        for file in pool.imap_unordered(self.download_file, self.links, maxsize=20):
            # print("Yielded: " + file[0])
            yield file[0], file[1]


class ZipDownloader(zipstream.ZipFile):
    def __init__(self, fileobj=None, mode="w", compression=ZIP_DEFLATED, allowZip64=False):
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
                yield from self.__write(**kwargs)
            if self.links:
                downloader = Downloader(self.links)
                for file in downloader:
                    yield from self._ZipFile__write(arcname=file[0], iterable=file[1],
                                                    buffer_size=self.links_buffersize,
                                                    compress_type=self.links_compress_type)
                    file[1].close()
        except Exception as e:
            print(e)
            raise
