FROM python:3

COPY requirements.txt /artmaster/requirements.txt

WORKDIR /artmaster

RUN pip install -r requirements.txt

COPY . .

WORKDIR /artmaster/artmaster

CMD python main.py