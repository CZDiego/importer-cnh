FROM python:3.6

RUN pip install pandas

ADD src/main.py /

CMD [ "python", "./main.py" ]