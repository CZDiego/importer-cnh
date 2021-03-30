# Run like:
# python3 excel.py

import pandas
import json
from variables import *

# TODO: Read excel file from local volume instead of having it in docker container
EXCEL_PATH = r'/export-content-20210302121846.xlsx'


def parse_pieces_of_content(path):

    result = []
    excel_data = pandas.read_excel(path)

    for index, row in excel_data.iterrows():
        for piece_of_content in PIECES_OF_CONTENT:

            if pandas.isnull(row[piece_of_content.columns["master_id"]]):
                continue

            ans = dict()
            for column_name, column_mapping in piece_of_content.columns.items():
                ans[column_name] = None if pandas.isnull(row[column_mapping]) else row[column_mapping]
            ans[AUTH_TEMPLATE] = piece_of_content.auth_template
            result.append(ans)

    return result


pieces_of_content = parse_pieces_of_content(EXCEL_PATH)

json_data = json.dumps(pieces_of_content)

print(json_data)
