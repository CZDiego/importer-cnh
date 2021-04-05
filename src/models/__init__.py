import json


class PieceOfContent(object):
    def __init__(self, **kwargs):
        self.path = kwargs.get("path", None)
        self.contentLibraryName = kwargs.get("contentLibraryName", None)
        self.authoringTemplateName = kwargs.get("authoringTemplateName", None)
        self.name = kwargs.get("name", None)
        self.title = kwargs.get("title", None)
        self.approvers = kwargs.get("approvers", None)
        self.categories = kwargs.get("categories", None)
        self.description = kwargs.get("description", None)
        self.creationDate = kwargs.get("creationDate", None)
        self.expiryDate = kwargs.get("expiryDate", None)
        self.generalDateOne = kwargs.get("generalDateOne", None)
        self.generalDateTwo = kwargs.get("generalDateTwo", None)
        self.keywords = kwargs.get("keywords", None)
        self.owners = kwargs.get("owners", None)
        self.authors = kwargs.get("authors", None)
        self.effectiveDate = kwargs.get("effectiveDate", None)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Resource(PieceOfContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Title = kwargs.get("Title", None)
        self.File = kwargs.get("File", None)
        self.description = kwargs.get("description", None)
        self.Image = kwargs.get("Image", None)
        self.targetAudienceByDealership = kwargs.get("targetAudienceByDealership", None)
        self.targetAudienceByBrand = kwargs.get("targetAudienceByBrand", None)
        self.targetAudienceByRole = kwargs.get("targetAudienceByRole", None)
        self.targetAudienceByCountry = kwargs.get("targetAudienceByCountry", None)
        self.relatedHubs = kwargs.get("relatedHubs", None)
        self.Publisher = kwargs.get("Publisher", None)
        self.Content_Type = kwargs.get("Content_Type", None)
        self.Topics = kwargs.get("Topics", None)


class CollapsibleElement(object):
    def __init__(self, title, body_elements, title_level=3):
        self.title_level = title_level
        self.title = title
        self.body_elements = body_elements
