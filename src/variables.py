import configparser

config = configparser.ConfigParser()
config.read("config.ini")

IMPORTER_SERVICE_VARIABLES = config["IMPORTER_SERVICE_VARIABLES"]
WEBSPHERE_VARIABLES = config["WEBSPHERE_VARIABLES"]
CONTENT_MAPPING_VARIABLES = config["CONTENT_MAPPING_VARIABLES"]


AUTH_TEMPLATE = "authoringTemplateName"
CONTENT_TYPE = "contentType"
RESOURCE = "Resource"
