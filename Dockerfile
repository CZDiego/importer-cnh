FROM python:3.6

RUN pip install requests
RUN pip install pandas
RUN pip install xlrd==1.2.0

ADD data/export-content-20210302121846.xlsx /
ADD src/variables.py /
ADD src/service/ /service
ADD src/config.ini /
ADD src/main.py /

CMD [ "python", "./main.py" ]
