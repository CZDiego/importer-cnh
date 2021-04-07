import configparser
from models import Resource

config = configparser.ConfigParser()
config.read("config.ini")

IMPORTER_SERVICE_VARIABLES = config["IMPORTER_SERVICE_VARIABLES"]
WEBSPHERE_VARIABLES = config["WEBSPHERE_VARIABLES"]
CONTENT_MAPPING_VARIABLES = config["CONTENT_MAPPING_VARIABLES"]


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

    # Add post files for each post
    for j in range(1, 6):

        post_file = Resource(masterId="Post " + str(i) + " File " + str(j) + " title",
                             authoringTemplateName="id_pays",
                             name="Post " + str(i) + " File " + str(j) + " title",
                             title="Post " + str(i) + " File " + str(j) + " title",
                             geographyVisibility="id_pays",
                             brandContractVisibility="theme",
                             targetingRole="Post " + str(i) + " File " + str(j) + " Targets",
                             contentLibraryName="langue",
                             linkURL="Post " + str(i) + " File " + str(j) + " LINK",
                             overrideLink="Post " + str(i) + " File " + str(j) + " URL",
                             path="Post " + str(i) + " Banner")

        PIECES_OF_CONTENT_MAPPING.append(DataMapping(post_file, RESOURCE, "post_file"))

    post = Resource(masterId="Post " + str(i) + " master id",
                    authoringTemplateName="id_pays",
                    name="Post " + str(i) + " Title",
                    title="Post " + str(i) + " Title",
                    description="Post " + str(i) + " Description",
                    geographyVisibility="id_pays",
                    brandContractVisibility="theme",
                    targetingRole="Post " + str(i) + " Targets",
                    contentLibraryName="langue",
                    creationDate="Post " + str(i) + " created",
                    path="Post " + str(i) + " Banner",
                    thumbnail="Post " + str(i) + " Thumbnail",
                    image="Post " + str(i) + " Banner")

    PIECES_OF_CONTENT_MAPPING.append(DataMapping(post, RESOURCE, "post"))


