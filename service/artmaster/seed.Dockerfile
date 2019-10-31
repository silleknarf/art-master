FROM python:3

COPY requirements.txt /artmaster/requirements.txt

WORKDIR /artmaster

RUN pip install -r requirements.txt

COPY . .

WORKDIR /artmaster/artmaster/database

RUN chmod +x wait-for-it.sh

CMD ./wait-for-it.sh db:3306 --strict --timeout=300 -- python create_database.py --dev