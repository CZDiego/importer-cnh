import json


class PieceOfContent(object):
    def __init__(self, **kwargs):
        self.path = kwargs.get("path")
        self.contentLibraryName = kwargs.get("contentLibraryName")
        self.authoringTemplateName = kwargs.get("authoringTemplateName")
        self.name = kwargs.get("name")
        self.title = kwargs.get("title")
        self.approvers = kwargs.get("approvers")
        self.categories = kwargs.get("categories")
        self.description = kwargs.get("description")
        self.creationDate = kwargs.get("creationDate")
        self.expiryDate = kwargs.get("expiryDate")
        self.generalDateOne = kwargs.get("generalDateOne")
        self.generalDateTwo = kwargs.get("generalDateTwo")
        self.keywords = kwargs.get("keywords")
        self.owners = kwargs.get("owners")
        self.authors = kwargs.get("authors")
        self.effectiveDate = kwargs.get("effectiveDate")

    def to_dict(self):
        return {
            k: v
            for k, v in self.__dict__.items()
            if v is not None
        }


class Resource(PieceOfContent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.masterId = kwargs.get("masterId", None)
        self.file = kwargs.get("file", None)
        self.image = kwargs.get("image", None)
        self.targetAudienceByDealership = kwargs.get("targetAudienceByDealership", None)
        self.targetAudienceByBrand = kwargs.get("targetAudienceByBrand", None)
        self.targetAudienceByRole = kwargs.get("targetAudienceByRole", None)
        self.targetAudienceByCountry = kwargs.get("targetAudienceByCountry", None)
        self.relatedHubs = kwargs.get("relatedHubs", None)
        self.publisher = kwargs.get("publisher", None)
        self.contentType = kwargs.get("contentType", None)
        self.topics = kwargs.get("topics", None)


class CollapsibleElement(object):
    def __init__(self, title, body_elements, title_level=3):
        self.title_level = title_level
        self.title = title
        self.body_elements = body_elements


class HTMLElement(object):
    def __init__(self, text, attrs, tag_name="p"):
        self.tag_name = tag_name
        self.text = text
        self.attrs = attrs


class CampaignHTMLBodyTemplate(object):
    def __init__(self, description, wysiwyg, collapsible_elements):
        self.description = description
        self.wysiwyg = wysiwyg
        self.collapsible_elements = collapsible_elements
