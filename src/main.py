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

authoringTemplateName = "CNH_File"
contentLibraryName = "Web Content"
path = "test"

try:
    kit1 = HTMLElement("Google", tag_name="a", attrs={"href": "https://www.google.com"})
    kit2 = HTMLElement("Facebook", tag_name="a", attrs={"href": "https://www.facebook.com"})
    kit3 = HTMLElement("Instagram", tag_name="a", attrs={"href": "https://www.instagram.com"})
    kit4 = HTMLElement("Apple", tag_name="a", attrs={"href": "https://www.apple.com"})
    post = Resource(name="post-7", title="Post 7", authoringTemplateName=authoringTemplateName,
                    contentLibraryName=contentLibraryName, path=path)
    post2 = Resource(name="post-8", title="Post 8", authoringTemplateName=authoringTemplateName,
                     contentLibraryName=contentLibraryName, path=path)
    result_post_1 = importer_service.save_item(post.to_dict())
    result_post_2 = importer_service.save_item(post2.to_dict())
    related_post_1 = HTMLElement(result_post_1.get("title", ""), tag_name="a",
                                 attrs={"href": utils.create_websphere_link(result_post_1.get("newId", ""),
                                                                            result_post_1.get("path", ""))})
    related_post_2 = HTMLElement(result_post_2.get("title", ""), tag_name="a",
                                 attrs={"href": utils.create_websphere_link(result_post_2.get("newId", ""),
                                                                            result_post_2.get("path", ""))})
    kit_file1 = HTMLElement("ADAM - Quick Guide 1 0", tag_name="a",
                            attrs={"href": WEBSPHERE_VARIABLES.get("StorageAPIBaseURL") + "ADAM - Quick Guide 1 0.pdf"})
    kit_file2 = HTMLElement("DP_home.html", tag_name="a",
                            attrs={"href": WEBSPHERE_VARIABLES.get("StorageAPIBaseURL") + "DP_home.html"})
    collapsible_elements = [CollapsibleElement("My first title", [kit1, kit2]),
                            CollapsibleElement("My second title", [kit3, kit4]),
                            CollapsibleElement("Related Content", [related_post_1, related_post_2]),
                            CollapsibleElement("LGF Space", [kit_file1, kit_file2])]
    campaign_body = CampaignHTMLBodyTemplate("Awesome Description", "<pre>This the WYSIWYG</pre>", collapsible_elements)
    page = html_markup_generator.generate(campaign_body, template_name=TemplateNames.CAMPAIGN.value)
    campaign = Resource(name="campaign-11", title="Campaign 11", authoringTemplateName=authoringTemplateName,
                        contentLibraryName=contentLibraryName, path=path, description=str(page))
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
