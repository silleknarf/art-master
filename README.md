[![CircleCI](https://circleci.com/gh/silleknarf/art-master.svg?style=shield)](https://circleci.com/gh/silleknarf/art-master)

README
======

Art Master is a game where players are pitted against each other to rapidly create art for the other players to critique! 

TODO
====

[Trello TODO Board](https://trello.com/b/xC2SMsIk/art-master)

CONTRIBUTING
============

Art Master is written in python and JS backed by a MySQL database.

Get the code:

    git clone https://github.com/silleknarf/art-master.git

## Backend

Install the dependencies:

    cd services/artmaster
    pip install -r requirements.txt
    
Turn off tracking of the user_config.py file:

    git update-index --assume-unchanged art-master/service/src/user_config.py

Populate the file below with your MySQL credentials:

    art-master/service/artmaster/artmaster/user_config.py

Set up the `art-master` database using the script at:

    cd art-master/service/artmaster/artmaster/database
    ./create_database.py --dev

Run the service:
    
    cd art-master/service/artmaster/artmaster
    ./app.py

To update the data model:

    cd art-master/service/src/database/
    ./generate_data_model.sh

To run the tests

    cd art-master/service/artmaster
    python -m unittest discover

## Frontend

Install the dependencies:

- npm
- yarn

Build:

    cd art-master/ui/
    yarn

Run:

    npm start