# Run like:
# python3 excel.py

import pandas
import json
from variables import *
import html_markup_utils.html_markup_generator as html_markup_generator
import service.importer_service as importer_service
from models import CollapsibleElement, Resource, HTMLElement, CampaignHTMLBodyTemplate

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
kit1 = HTMLElement("Google", tag_name="a", attrs={"href": "www.google.com"})
kit2 = HTMLElement("Facebook", tag_name="a", attrs={"href": "www.facebook.com"})
kit3 = HTMLElement("Instagram", tag_name="a", attrs={"href": "www.instagram.com"})
kit4 = HTMLElement("Apple", tag_name="a", attrs={"href": "www.apple.com"})
collapsible_elements = [CollapsibleElement("My first title", [kit1, kit2]),
                        CollapsibleElement("My second title", [kit3, kit4])]
campaign_body = CampaignHTMLBodyTemplate("Awesome Description", "<pre>This the WYSIWYG</pre>", collapsible_elements)
page = html_markup_generator.generate(campaign_body, template_name=TemplateNames.CAMPAIGN.value)
campaign = Resource(name="campaign", title="Campaign", authoringTemplateName="CNH_File",
                    contentLibraryName="Web Content", path="test", description=str(page))
print(json_data)
print("-------------------------------------------")
print(page)
print(campaign.__dict__)
print(importer_service.save_item(campaign.to_dict()))
