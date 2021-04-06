import re
import variables

AssetsWebSphereBaseURL = variables.WEBSPHERE_VARIABLES.get("AssetsWebSphereBaseURL")


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
