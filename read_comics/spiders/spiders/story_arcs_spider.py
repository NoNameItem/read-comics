from .base_spider import BaseSpider


class StoryArcsSpider(BaseSpider):
    # LIST_URL_PATTERN should contain 3 placeholders: limit, offset and api_key and should not contain filter parameter
    LIST_URL_PATTERN = "https://comicvine.gamespot.com/api/story_arcs?" \
                       "format=json&" \
                       "field_list=api_detail_url,id&" \
                       "sort=id:asc&" \
                       "offset={offset}&" \
                       "limit={limit}&" \
                       "api_key={api_key}"
    name = "comicvine_story_arcs"
    DETAIL_FIELD_LIST = \
        "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,first_appeared_in_issue,publisher"
