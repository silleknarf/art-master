FROM python:3

WORKDIR /artmaster

RUN pip install mysqlclient
RUN pip install sqlacodegen

CMD sqlacodegen mysql://root:root@db/art-master-dev > artmaster/database/data_model.py
