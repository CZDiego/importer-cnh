import configparser

config = configparser.ConfigParser()
config.read("config.ini")

IMPORTER_SERVICE_VARIABLES = config["IMPORTER_SERVICE_VARIABLES"]

class DataMapping:
    def __init__(self, columns, auth_template):
        self.columns = columns
        self.auth_template = auth_template


class PoCMapping:
    def __init__(self, auth_template, master_id, name, description):
        self.auth_template = auth_template
        self.master_id = master_id
        self.name = name
        self.description = description

    def toDataMapping(self):
        columns = dict(master_id=self.master_id, name=self.name, description=self.description)
        return DataMapping(columns, self.auth_template)


PIECES_OF_CONTENT = []
AUTH_TEMPLATE = "auth-template"

PIECES_OF_CONTENT.append(PoCMapping("post", "Post 1 master id", "Post 1 Title", "Post 1 Description").toDataMapping())
PIECES_OF_CONTENT.append(PoCMapping("post", "Post 2 master id", "Post 2 Title", "Post 2 Description").toDataMapping())
PIECES_OF_CONTENT.append(PoCMapping("post", "Post 3 master id", "Post 3 Title", "Post 3 Description").toDataMapping())
PIECES_OF_CONTENT.append(PoCMapping("post", "Post 4 master id", "Post 4 Title", "Post 4 Description").toDataMapping())
PIECES_OF_CONTENT.append(PoCMapping("post", "Post 5 master id", "Post 5 Title", "Post 5 Description").toDataMapping())
