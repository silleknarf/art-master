[![CircleCI](https://circleci.com/gh/silleknarf/art-master.svg?style=shield)](https://circleci.com/gh/silleknarf/art-master)

README
======

Art Master is a game where players are pitted against each other to rapidly create art for the other players to critique! 

TODO
====

Development in progress!

[Trello TODO Board](https://trello.com/b/xC2SMsIk/art-master)

CONTRIBUTING
============

Art Master is written in python and JS backed by a MySQL database. It can be running as a collection of docker containers using docker-compose.

Get the code:

    git clone https://github.com/silleknarf/art-master.git

Getting Started
===============

Seed the `art-master` database:

    docker-compose up -d --build seed

Start the db, service and UI:

    docker-compose up -d --build ui
    Open browser with url: http://localhost:3000

To update the data model:

    docker-compose up -d --build generate_data_model

To run the tests:

    cd art-master/service/artmaster
    python -m unittest discover

Run Storybook:

    docker-compose up -d --build storybook
    Open browser with url: http://localhost:9009
