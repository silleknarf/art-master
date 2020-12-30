FROM python:3

WORKDIR /artmaster

RUN pip install mysqlclient
RUN pip install sqlacodegen

CMD sqlacodegen mysql://root:$CRAICBOX_DATABASE_PASSWORD@db/craicbox > artmaster/database/data_model.py
