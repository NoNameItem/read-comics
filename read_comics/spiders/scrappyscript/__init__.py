"""
Run scrapy spiders from a script.

Blocks and runs all requests in parallel.  Accumulated items from all
spiders are returned as a list.
"""

import collections

from billiard import Process  # fork of multiprocessing that works with celery
from billiard.queues import Queue
from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


class ScrapyScriptException(Exception):
    pass


class Job:  # noqa SIM119
    """A job is a single request to call a specific spider. *args and **kwargs
    will be passed to the spider constructor.
    """

    def __init__(self, spider, *args, **kwargs):
        """Parms:
        spider (spidercls): the spider to be run for this job.
        """
        self.spider = spider
        self.args = args
        self.kwargs = kwargs


class Processor(Process):
    """Start a twisted reactor and run the provided scrapy spiders.
    Blocks until all have finished.
    """

    def __init__(self, settings=None, ignore_results=True):
        """
        Parms:
          settings (scrapy.settings.Settings) - settings to apply.  Defaults
        to Scrapy default settings.
        """
        kwargs = {"ctx": __import__("billiard.synchronize")}

        self.ignore_results = ignore_results

        self.results = Queue(**kwargs)
        self.items = []
        self.settings = settings or Settings()
        dispatcher.connect(self._item_scraped, signals.item_scraped)

    def _item_scraped(self, item):
        if not self.ignore_results:
            self.items.append(item)

    def _crawl(self, requests):
        """
        Parameters:
            requests (Request) - One or more Jobs. All will
                                 be loaded into a single invocation of the reactor.
        """
        self.crawler = CrawlerProcess(self.settings)

        # crawl can be called multiple times to queue several requests
        for req in requests:
            self.crawler.crawl(req.spider, *req.args, **req.kwargs)

        self.crawler.start()
        self.crawler.stop()
        if not self.ignore_results:
            self.results.put(self.items)

    def run(self, jobs):
        """Start the Scrapy engine, and execute all jobs.  Return consolidated results
        in a single list.

        Parms:
          jobs ([Job]) - one or more Job objects to be processed.

        Returns:
          List of objects yielded by the spiders after all jobs have run.
        """
        if not isinstance(jobs, collections.abc.Iterable):
            jobs = [jobs]
        self.validate(jobs)

        results = []

        p = Process(target=self._crawl, args=[jobs])
        p.start()
        if not self.ignore_results:
            results = self.results.get()  # noqa R504
        p.join()
        p.terminate()

        return results  # noqa R504

    def validate(self, jobs):
        if not all([isinstance(x, Job) for x in jobs]):
            raise ScrapyScriptException("scrapyscript requires Job objects.")
