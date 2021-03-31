# Run like:
# python3 excel.py

import pandas
import json
from variables import *
from service.importerservice import *

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

piece_of_content = dict(name="test-from-docker-2",title="Test From Docker2",authoringTemplateName="CNH_File",contentLibraryName="Web Content",path="test")
data = []
data.append(piece_of_content)
payload = dict(data=data)
print(payload)
print(json_data)
print(ImporterService.saveItem(payload))