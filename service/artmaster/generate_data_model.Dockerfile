FROM python:3

WORKDIR /artmaster

RUN pip install mysqlclient
RUN pip install sqlacodegen

CMD sqlacodegen mysql://root:$CRAICBOX_DATABASE_PASSWORD@db/art-master-dev > artmaster/database/data_model.py
