README
======

Art Master is a game where players are pitted against each other to rapidly create art for the other players to critique! 

CONTRIBUTING
============

Art Master is written in python and JS backed by a MySQL database.

Get the code:

    git clone https://github.com/silleknarf/art-master.git

## Backend

Install the dependencies:

- python
- flask
- MySQL
- SQLAlchemy
- sqlacodegen

Set up the `art-master` database using the script at:

    art-master/src/database/database_schema.sql

Run:
    
    cd art-master/service/src
    ./app.py

To update the data model:

    cd art-master/service/src/database/
    ./generate_data_model.sh

## Frontend

Install the dependencies:

- npm
- yarn

Build:

    cd art-master/ui/
    yarn

Run:

    npm run