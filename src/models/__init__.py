from enum import Enum


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
        self.wysiwyg = kwargs.get("wysiwyg")
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


class CommonAuthoringTemplate(PieceOfContent):
    def __init__(self, authoringTemplateName, contentLibraryName, path, name, title, **kwargs):
        super().__init__(authoringTemplateName, contentLibraryName, path, name, title, **kwargs)
        self.brandContractVisibility = kwargs.get("brandContractVisibility", None)
        self.geographyVisibility = kwargs.get("geographyVisibility", None)
        self.dealershipVisibility = kwargs.get("dealershipVisibility", None)
        self.dealershipTypeVisibility = kwargs.get("dealershipTypeVisibility", None)
        self.roleVisibility = kwargs.get("roleVisibility", None)
        self.contentAuditor = kwargs.get("contentAuditor", None)
        self.shortTitle = kwargs.get("shortTitle", None)
        self.summary = kwargs.get("summary", None)
        self.masterId = kwargs.get("masterId", None)
        self.thumbnail = kwargs.get("thumbnail", None)
        self.thumbnailCaption = kwargs.get("thumbnailCaption", None)
        self.alternateByline = kwargs.get("alternateByline", None)
        self.image = kwargs.get("image", None)
        self.imageCaption = kwargs.get("imageCaption", None)
        self.body = kwargs.get("body", None)
        self.attachment = kwargs.get("attachment", None)
        self.downloads = kwargs.get("downloads", None)
        self.moreInformation = kwargs.get("moreInformation", None)
        self.relatedContent = kwargs.get("relatedContent", None)
        self.notifySubscribers = kwargs.get("notifySubscribers", None)
        self.sidebarComponent1 = kwargs.get("sidebarComponent1", None)
        self.sidebarComponent2 = kwargs.get("sidebarComponent2", None)
        self.sidebarComponent3 = kwargs.get("sidebarComponent3", None)
        self.pageType = kwargs.get("pageType", None)
        self.pageTitle = kwargs.get("pageTitle", None)
        self.contentType = kwargs.get("contentType", None)
        self.topics = kwargs.get("topics", None)
        self.targetingRole = kwargs.get("targetingRole", None)
        self.siteLocation = kwargs.get("siteLocation", None)
        self.mlTranslationsTable = kwargs.get("mlTranslationsTable", None)
        self.topComponent = kwargs.get("topComponent", None)
        self.bottomComponent = kwargs.get("bottomComponent", None)


class Resource(CommonAuthoringTemplate):
    def __init__(self, authoringTemplateName, contentLibraryName, path, name, title, **kwargs):
        super().__init__(authoringTemplateName, contentLibraryName, path, name, title, **kwargs)
        self.icon = kwargs.get("icon", None)
        self.transformHeadersH2 = kwargs.get("transformHeadersH2", None)
        self.transformHeadersH3 = kwargs.get("transformHeadersH3", None)
        self.scopeSection = kwargs.get("scopeSection", None)
        self.linkURL = kwargs.get("linkURL", None)
        self.overrideLink = kwargs.get("overrideLink", None)
        self.attachmentContentDescription = kwargs.get("attachmentContentDescription", None)
        self.attachmentImage = kwargs.get("attachmentImage", None)
        self.relatedHubs = kwargs.get("relatedHubs", None)
        self.overrideAudiences = kwargs.get("overrideAudiences", None)


class News(CommonAuthoringTemplate):
    def __init__(self, authoringTemplateName, contentLibraryName, path, name, title, **kwargs):
        super().__init__(authoringTemplateName, contentLibraryName, path, name, title, **kwargs)
        self.attachmentDescription = kwargs.get("attachmentDescription", None)


class CollapsibleElement(object):
    def __init__(self, title, body_elements, title_level=3):
        self.title_level = title_level
        self.title = title
        self.body_elements = body_elements


class HTMLElement(object):
    def __init__(self, tag_name, text=None, attrs=None):
        if attrs is None:
            attrs = {}
        self.tag_name = tag_name
        self.text = text
        self.attrs = attrs


class CampaignHTMLBodyTemplate(object):
    def __init__(self, description, wysiwyg, collapsible_elements):
        self.description = description
        self.wysiwyg = wysiwyg
        self.collapsible_elements = collapsible_elements


class DealershipTypes(Enum):
    DEALER = "Dealer"
    SUB_DEALER = "Sub-Dealer"


class TransformHeaders(Enum):
    AS_TYPED = "As Typed"
    COLLAPSIBLE_SECTIONS = "Collapsible Sections"
