import PieceOfContent


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
