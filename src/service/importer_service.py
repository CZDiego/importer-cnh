from . import http_client
from variables import IMPORTER_SERVICE_VARIABLES

BASE_URL = IMPORTER_SERVICE_VARIABLES.get("BaseURL")
IMPORT_CONTENT_URL = BASE_URL + IMPORTER_SERVICE_VARIABLES.get("ImporterURL")


def post_items(data):
    payload = dict(data=data)
    return http_client.post(IMPORT_CONTENT_URL, payload)


def save_item(piece_of_content):
    data = [piece_of_content]
    return post_items(data)


def save_items(data):
    return post_items(data)
