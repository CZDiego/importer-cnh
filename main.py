#Run like:
#python3 excel.py

import pandas

EXCEL_PATH = r'/Users/diegocontreras/Documents/export-content-20210302121846 - excel - with GDP fields v2.xlsx'

def readExcel(path):

	excelData = pandas.read_excel (path)

	for index, row in excelData.iterrows():

		print(row)


readExcel(EXCEL_PATH)
