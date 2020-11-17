[![CircleCI](https://circleci.com/gh/silleknarf/craicbox.svg?style=shield)](https://circleci.com/gh/silleknarf/craicbox)

README
======

Craicbox is a game where players are pitted against each other to rapidly create art for the other players to critique!

TODO
====

Development in progress!

[Trello TODO Board](https://trello.com/b/xC2SMsIk/craicbox)

CONTRIBUTING
============

Craicbox is written in python and JS backed by a MySQL database. It can be running as a collection of docker containers using docker-compose.

Get the code:

    git clone https://github.com/silleknarf/craicbox.git

Getting Started
===============

Create a `.env` file in the root directory of the project and set the variable below:

    CRAICBOX_DATABASE_PASSWORD=<password>
    SOCKETIO_PASSWORD=<password>

Seed the `craicbox` database:

    docker-compose up -d --build seed

Start the db, service and UI:

    docker-compose up -d --build ui
    Open browser with url: http://localhost:3000

To update the data model:

    docker-compose up -d --build generate_data_model

To run the tests:

    docker-compose up --build service_tests

Run Storybook:

    docker-compose up -d --build storybook
    Open browser with url: http://localhost:9009

Production Setup
================

1. Set up a kubernetes cluster which has got at least one persistent volume and node
1. Push the images for seed, service and UI up to an image registry
1. Add a secret for the image registry used
    `kubectl create secret docker-registry regcred --docker-server=rg.nl-ams.scw.cloud/craicbox --docker-username=nologin --docker-password=<your_password> --docker-email=<your_email> -n craicbox`
1. Add a secret called mysql-secrets with a value in data for the key: mysql-root-password
1. Update the k8s templates to point the registry images
1. Run in all the k8s templates
