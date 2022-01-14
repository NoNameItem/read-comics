import re

import boto3
from django.conf import settings

ONE_LEVEL_REGEX = re.compile(r"^[^\/]+\/?$")


def get_level(prefix=''):
    session = boto3.session.Session()
    s3 = session.resource('s3', region_name=settings.DO_SPACE_DATA_REGION,
                          endpoint_url=settings.DO_SPACE_DATA_ENDPOINT_URL,
                          aws_access_key_id=settings.DO_SPACE_DATA_KEY,
                          aws_secret_access_key=settings.DO_SPACE_DATA_SECRET)
    bucket = s3.Bucket(settings.DO_SPACE_DATA_BUCKET)

    response = bucket.meta.client.list_objects(
        Bucket=bucket.name, Delimiter='/', Prefix=prefix
    )
    next_marker = response.get("NextMarker")
    common_prefixes = response.get("CommonPrefixes")
    contents = response.get("Contents")
    if common_prefixes:
        data = [(x["Prefix"], 0) for x in common_prefixes]
    else:
        data = [(x['Key'], x["Size"]) for x in contents[1:]]

    while next_marker:
        response = bucket.meta.client.list_objects(
            Bucket=bucket.name, Delimiter='/', Prefix=prefix, Marker=next_marker
        )
        next_marker = response.get("NextMarker")
        common_prefixes = response.get("CommonPrefixes")
        contents = response.get("Contents")
        if common_prefixes:
            data += [x["Prefix"] for x in common_prefixes]
        else:
            data += [x['Key'] for x in contents]

    s3objects = [
        {"name": x[0].removeprefix(prefix), "full_name": x[0], "size": x[1]}
        for x in data
        if not x[0].removeprefix(prefix).startswith(".")
    ]

    s3objects.sort(key=lambda x: x['name'])

    return s3objects
