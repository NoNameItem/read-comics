from .base_spider import BaseSpider


class PowersSpider(BaseSpider):
    # LIST_URL_PATTERN should contain 3 placeholders: limit, offset and api_key and should not contain filter parameter
    LIST_URL_PATTERN = (
        "https://comicvine.gamespot.com/api/powers/?"
        "format=json&"
        "field_list=id,api_detail_url,site_detail_url,name,aliases&"
        "sort=id:asc&"
        "offset={offset}&"
        "limit={limit}&"
        "api_key={api_key}"
    )
    name = "comicvine_powers"
    DETAIL_FIELD_LIST = "id,api_detail_url,site_detail_url,name,aliases,description"
