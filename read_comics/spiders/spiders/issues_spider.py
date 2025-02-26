from .base_spider import BaseSpider


class IssuesSpider(BaseSpider):
    # LIST_URL_PATTERN should contain 3 placeholders: limit, offset and api_key and should not contain filter parameter
    LIST_URL_PATTERN = (
        "https://comicvine.gamespot.com/api/issues/?"
        "format=json&"
        "field_list=id,api_detail_url,site_detail_url,name,aliases,deck,image,issue_number,cover_date,associated_images"
        "store_date,volume&"
        "sort=id:asc&"
        "offset={offset}&"
        "limit={limit}&"
        "api_key={api_key}"
    )
    name = "comicvine_issues"
    DETAIL_FIELD_LIST = (
        "id,api_detail_url,site_detail_url,name,aliases,deck,description,image,issue_number,"
        "cover_date,store_date,character_credits,character_died_in,concept_credits,location_credits,"
        "object_credits,person_credits,story_arc_credits,team_credits,team_disbanded_in,volume,associated_images"
    )
