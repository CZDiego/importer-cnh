from . import http_client
from variables import IMPORTER_SERVICE_VARIABLES
import utils

BASE_URL = IMPORTER_SERVICE_VARIABLES.get("BaseURL")
IMPORT_CONTENT_URL = BASE_URL + IMPORTER_SERVICE_VARIABLES.get("ImporterURL")
USER = IMPORTER_SERVICE_VARIABLES.get("User")
PASSWORD = IMPORTER_SERVICE_VARIABLES.get("Password")


def post_items(data, user=None, password=None):
    payload = dict(data=data)
    if user is not None: payload["user"] = user
    if password is not None: payload["password"] = password
    return http_client.post(IMPORT_CONTENT_URL, payload)


def save_item(piece_of_content, user=USER, password=PASSWORD):
    data = [piece_of_content]
    response = post_items(data)
    result = utils.get_result(response)
    errors = result.get("errors")
    if len(errors) > 0:
        result = update_item(piece_of_content, user, password)
    return result


def update_items(data, user=USER, password=PASSWORD):
    return post_items(data, user=user, password=password)


def save_items(data, user=USER, password=PASSWORD):
    response = post_items(data)
    report = utils.get_report()
    for item in report:
        errors = item.get("errors")
        if len(errors) > 0:
            response = update_items(data, user, password)
            break
    return response


def update_item(piece_of_content, user=USER, password=PASSWORD):
    data = [piece_of_content]
    response = post_items(data, user=user, password=password)
    return utils.get_result(response)


def save_items(data):
    return post_items(data)
