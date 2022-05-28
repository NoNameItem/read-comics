from .base_spider import BaseSpider


class PeopleSpider(BaseSpider):
    # LIST_URL_PATTERN should contain 3 placeholders: limit, offset and api_key and should not contain filter parameter
    LIST_URL_PATTERN = "https://comicvine.gamespot.com/api/people?" \
                       "format=json&" \
                       "field_list=api_detail_url,id&" \
                       "sort=id:asc&" \
                       "offset={offset}&" \
                       "limit={limit}&" \
                       "api_key={api_key}"
    name = "comicvine_people"
    # Optimize field list
    DETAIL_FIELD_LIST = "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,birth,country,death," \
                        "hometown"
