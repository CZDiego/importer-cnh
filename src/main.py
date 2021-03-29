# Run like:
# python3 excel.py

import pandas

# TODO: Read excel file from local volume instead of having it in docker container
EXCEL_PATH = r'/export-content-20210302121846.xlsx'


def read_excel(path):
    excel_data = pandas.read_excel(path)

    for index, row in excel_data.iterrows():
        print(row)


read_excel(EXCEL_PATH)

print("Hello world")
