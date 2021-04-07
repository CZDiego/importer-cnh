import configparser
from models import Resource

config = configparser.ConfigParser()
config.read("config.ini")

IMPORTER_SERVICE_VARIABLES = config["IMPORTER_SERVICE_VARIABLES"]
WEBSPHERE_VARIABLES = config["WEBSPHERE_VARIABLES"]


class DataMapping:
    def __init__(self, properties, auth_template, content_type):
        self.properties = properties
        self.auth_template = auth_template
        self.content_type = content_type


PIECES_OF_CONTENT_MAPPING = []
AUTH_TEMPLATE = "authoringTemplateName"
CONTENT_TYPE = "contentType"
RESOURCE = "Resource"

# Add posts
for i in range(1, 6):

    # Add post files
    for j in range(1, 6):
        post_file = Resource(masterId="Post 1 File 1 title", title="Post 1 File 1 title",
                             targetAudienceByRole="Post 1 File 1 Targets")
    post = Resource(masterId="Post " + str(i) + " master id", title="Post " + str(i) + " Title",
                    description="Post " + str(i) + " Description", targetAudienceByCountry="id_pays",
                    targetAudienceByBrand="theme", contentLibraryName="langue", creationDate="Post 1 created",
                    name="Post " + str(i) + " Title", path="Post " + str(i) + " Banner", authoringTemplateName="id_pays")
    PIECES_OF_CONTENT_MAPPING.append(DataMapping(post, RESOURCE, "post"))


