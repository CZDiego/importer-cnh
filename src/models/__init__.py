class PieceOfContent(object):
    def __init__(self, authoringTemplateName, contentLibraryName, path, name, title, **kwargs):
        self.authoringTemplateName = authoringTemplateName
        self.contentLibraryName = contentLibraryName
        self.path = path
        self.name = name
        self.title = title
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
    def __init__(self, authoringTemplateName, contentLibraryName, path, name, title, **kwargs):
        super().__init__(authoringTemplateName, contentLibraryName, path, name, title, **kwargs)
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
