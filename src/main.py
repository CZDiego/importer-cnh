# Run like:
# python3 excel.py

import pandas
import json
from variables import *
import html_markup_utils.html_markup_generator as html_markup_generator
import service.importer_service as importer_service
from models import CollapsibleElement, Resource

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
collapsible_elements = [CollapsibleElement("My first title", ["1:firstParagraph", "1:secondParagraph"]),
                        CollapsibleElement("My second title", ["2:firstParagraph", "2:secondParagraph"])]
page = html_markup_generator.generate(template_name=TemplateNames.CAMPAIGN.value, description="My description",
                                      collapsible_elements=collapsible_elements)
piece_of_content = Resource(name="test-from-docker-5", title="Test From Docker5", authoringTemplateName="CNH_File",
                            contentLibraryName="Web Content", path="test", description=str(page))
print(json_data)
print("-------------------------------------------")
print(page)
print(json.dumps(piece_of_content.to_json()))
print(importer_service.save_item(piece_of_content.to_json()))
