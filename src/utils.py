import re
import variables

AssetsWebSphereBaseURL = variables.WEBSPHERE_VARIABLES.get("AssetsWebSphereBaseURL")
CONTENT_MAPPING_VARIABLES = variables.CONTENT_MAPPING_VARIABLES


def create_websphere_link(uuid, path):
    if "/" not in path: return "#"
    last_index_of_slash = path.rindex("/")
    parent_path = path[:last_index_of_slash + 1]
    name = path[last_index_of_slash + 1:]
    parent_path = to_kebab_case(parent_path)
    query_params = "?"
    query_params += "contentIDR=" + uuid
    query_params += "&useDefaultText=1&useDefaultDesc=0"
    return AssetsWebSphereBaseURL + parent_path + name + query_params


def to_kebab_case(string):
    string = re.sub('\s', r'', string)
    string = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', string).lower()


def get_result(response):
    report = response.get("report", {})
    return report[0] if len(report) > 0 else {}


def get_mapped_value(key):
    key = key.lower()
    return CONTENT_MAPPING_VARIABLES.get(key)


def get_file_name_from_url(url):
    return "" if url is None else url.rsplit('/', 1)[-1]


def get_download_path(url):
    return "businessconnection/" + get_file_name_from_url(url)


def get_image_path(url):
    return "/appl/lfs/" + get_download_path(url)
