import logging
import json
from variables import *
import html_markup_utils.html_markup_generator as html_markup_generator
import service.importer_service as importer_service
from models import CollapsibleElement, Resource, HTMLElement, CampaignHTMLBodyTemplate
import utils
import service.preprocess as preprocessing

# TODO: Read excel file from local volume instead of having it in docker container
EXCEL_PATH = r'/export-content-20210302121846.xlsx'


# Main
pieces_of_content = preprocessing.get_pieces_of_content(EXCEL_PATH)

json_data = json.dumps(pieces_of_content, indent=2)

print(json_data)
print("-------------------------------------------")

TemplateNames = html_markup_generator.TemplateNames

authoringTemplateName = "Resource"
contentLibraryName = "content-english"
path = "cnhi/discover/internal/resources"

try:
    kit1 = HTMLElement("a", text="Google", attrs={"href": "https://www.google.com"})
    kit2 = HTMLElement("a", text="Facebook", attrs={"href": "https://www.facebook.com"})
    kit3 = HTMLElement("a", text="Instagram", attrs={"href": "https://www.instagram.com"})
    kit4 = HTMLElement("a", text="Apple", attrs={"href": "https://www.apple.com"})
    post = Resource(name="post-1", title="Post 1", authoringTemplateName=authoringTemplateName,
                    contentLibraryName=contentLibraryName, path=path, transformHeadersH3="Collapsible Sections")
    post2 = Resource(name="post-2", title="Post 2", authoringTemplateName=authoringTemplateName,
                     contentLibraryName=contentLibraryName, path=path, transformHeadersH3="Collapsible Sections")
    result_post_1 = importer_service.save_item(post.to_dict())
    result_post_2 = importer_service.save_item(post2.to_dict())
    related_post_1 = HTMLElement("a", text=result_post_1.get("title", ""),
                                 attrs={"href": utils.create_websphere_link(result_post_1.get("newId", ""),
                                                                            result_post_1.get("path", ""))})
    related_post_2 = HTMLElement("a", text=result_post_2.get("title", ""),
                                 attrs={"href": utils.create_websphere_link(result_post_2.get("newId", ""),
                                                                            result_post_2.get("path", ""))})
    kit_file1 = HTMLElement("a", text="20201208 CanadaContent (2) (1).json",
                            attrs={"href": WEBSPHERE_VARIABLES.get(
                                "StorageAPIBaseURL") + "20201208 CanadaContent (2) (1).json",
                                   "target": "_blank"})
    kit_file2 = HTMLElement("a", text="tbio_config (1).jsp",
                            attrs={"href": WEBSPHERE_VARIABLES.get("StorageAPIBaseURL") + "tbio_config (1).jsp",
                                   "target": "_blank"})
    collapsible_elements = [CollapsibleElement("My first title", [kit1, kit2]),
                            CollapsibleElement("My second title", [kit3, kit4]),
                            CollapsibleElement("Related Content", [related_post_1, related_post_2]),
                            CollapsibleElement("LGF Space", [kit_file1, kit_file2])]
    downloads = html_markup_generator.create_rich_text([kit_file1, kit_file2])
    related_content = html_markup_generator.create_rich_text([related_post_1, related_post_2])
    print("related_content")
    print(related_content)
    campaign_body = CampaignHTMLBodyTemplate("Awesome Description", "<pre>This the WYSIWYG</pre>", collapsible_elements)
    page = html_markup_generator.generate(campaign_body, template_name=TemplateNames.CAMPAIGN.value)
    campaign = Resource(name="campaign-1", title="Campaign 1", authoringTemplateName=authoringTemplateName,
                        contentLibraryName=contentLibraryName, path=path, body=str(page),
                        transformHeadersH3="Collapsible Sections", downloads=downloads, relatedContent=related_content)
    print("-------------------------------------------")
    print(page)
    result = importer_service.save_item(campaign.to_dict())
    print(result)
except (ConnectionError, Exception) as e:
    logging.exception(e)

print(utils.get_mapped_value("cih"))
print(utils.get_mapped_value("ADVANCED FARMING SYSTEMS"))
print(utils.get_mapped_value("UK"))

# print(json_data)


div = HTMLElement("div")
bannerTitle = HTMLElement("span", "Facebook Banners")
hr = HTMLElement("hr")
banner1 = HTMLElement("a", "Facebook Banner 1", dict(href="#"))
banner2 = HTMLElement("a", "Facebook Banner 2", dict(href="#"))

downloads = html_markup_generator.create_rich_text([div, bannerTitle, hr, banner1, banner2])
print(downloads)
