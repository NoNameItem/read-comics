from collections import OrderedDict
from math import ceil

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        if self.page is not None:
            return Response(
                OrderedDict(
                    [
                        ("count", self.page.paginator.count),
                        ("next", self.get_next_link()),
                        ("previous", self.get_previous_link()),
                        (
                            "pages_count",
                            ceil(self.page.paginator.count / (self.page_size or self.page.paginator.count)),
                        ),
                        ("results", data),
                    ]
                )
            )
        return data
