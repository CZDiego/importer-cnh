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


def parse_pieces_of_content(path):
    result = []
    excel_data = pandas.read_excel(path)

    for index, row in excel_data.iterrows():
        for piece_of_content_mapping in PIECES_OF_CONTENT_MAPPING:

            if pandas.isnull(row[piece_of_content_mapping.columns["master_id"]]):
                continue

            ans = dict()
            for column_name, column_mapping in piece_of_content_mapping.columns.items():
                ans[column_name] = None if pandas.isnull(row[column_mapping]) else row[column_mapping]
            ans[AUTH_TEMPLATE] = piece_of_content_mapping.auth_template
            result.append(ans)

    return result


# Main
pieces_of_content = parse_pieces_of_content(EXCEL_PATH)

json_data = json.dumps(pieces_of_content)

TemplateNames = html_markup_generator.TemplateNames
kit1 = HTMLElement("Google", tag_name="a", attrs={"href": "https://www.google.com"})
kit2 = HTMLElement("Facebook", tag_name="a", attrs={"href": "https://www.facebook.com"})
kit3 = HTMLElement("Instagram", tag_name="a", attrs={"href": "https://www.instagram.com"})
kit4 = HTMLElement("Apple", tag_name="a", attrs={"href": "https://www.apple.com"})
post = Resource(name="post-3", title="Post 3", authoringTemplateName="CNH_File",
                contentLibraryName="Web Content", path="test")
post2 = Resource(name="post-4", title="Post 4", authoringTemplateName="CNH_File",
                 contentLibraryName="Web Content", path="test")
response_post_1 = importer_service.save_item(post.to_dict())
response_post_2 = importer_service.save_item(post2.to_dict())
result_post_1 = utils.get_result(response_post_1)
result_post_2 = utils.get_result(response_post_2)
related_post_1 = HTMLElement(result_post_1.get("title", ""), tag_name="a",
                             attrs={"href": utils.create_websphere_link(result_post_1.get("newId", ""),
                                                                        result_post_1.get("path", ""))})
related_post_2 = HTMLElement(result_post_2.get("title", ""), tag_name="a",
                             attrs={"href": utils.create_websphere_link(result_post_2.get("newId", ""),
                                                                        result_post_2.get("path", ""))})
collapsible_elements = [CollapsibleElement("My first title", [kit1, kit2]),
                        CollapsibleElement("My second title", [kit3, kit4]),
                        CollapsibleElement("Related Content", [related_post_1, related_post_2])]
campaign_body = CampaignHTMLBodyTemplate("Awesome Description", "<pre>This the WYSIWYG</pre>", collapsible_elements)
page = html_markup_generator.generate(campaign_body, template_name=TemplateNames.CAMPAIGN.value)
campaign = Resource(name="campaign-9", title="Campaign 9", authoringTemplateName="CNH_File",
                    contentLibraryName="Web Content", path="test", description=str(page))
print(json_data)
print("-------------------------------------------")
print(page)
response = importer_service.save_item(campaign.to_dict())
result = utils.get_result(response)
print(result)
