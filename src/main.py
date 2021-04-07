# Run like:
# python3 excel.py

import pandas
import json
from variables import *
import html_markup_utils.html_markup_generator as html_markup_generator
import service.importer_service as importer_service
from models import CollapsibleElement, Resource, HTMLElement, CampaignHTMLBodyTemplate
import utils

# TODO: Read excel file from local volume instead of having it in docker container
EXCEL_PATH = r'/export-content-20210302121846.xlsx'


def is_json_serializable(value):

    try:
        json.dumps(value)
        return True
    except TypeError:
        return False


def parse_pieces_of_content(excel_path):
    pieces_of_content_result = []
    excel_data = pandas.read_excel(excel_path)

    for index, row in excel_data.iterrows():
        for piece_of_content_mapping in PIECES_OF_CONTENT_MAPPING:

            if pandas.isnull(row[piece_of_content_mapping.properties.masterId]):
                continue

            ans = dict()
            for column_name, column_mapping in piece_of_content_mapping.properties.__dict__.items():
                ans[column_name] = None if column_mapping is None or pandas.isnull(row[column_mapping]) \
                    else row[column_mapping]

                if not is_json_serializable(ans[column_name]):
                    ans[column_name] = str(ans[column_name])

            ans[AUTH_TEMPLATE] = piece_of_content_mapping.auth_template
            ans[CONTENT_TYPE] = piece_of_content_mapping.content_type
            pieces_of_content_result.append(ans)

    return pieces_of_content_result


# Main
pieces_of_content = parse_pieces_of_content(EXCEL_PATH)

json_data = json.dumps(pieces_of_content)

print(json_data)
print("-------------------------------------------")

TemplateNames = html_markup_generator.TemplateNames

authoringTemplateName = "CNH_File"
contentLibraryName = "Web Content"
path = "test"

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

print(page)
result = importer_service.save_item(campaign.to_dict())
print(result)
