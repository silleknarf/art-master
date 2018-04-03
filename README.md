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
- MySQL
- SQLAlchemy `pip install sqlalchemy`  
- flask `pip install Flask`
- sqlacodegen

Populate the user_config.py below with your MySQL credentials:

    art-master/src/user_config.py

Set up the `art-master` database using the script at:

    cd art-master/src/database
    ./create_database.py --dev

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