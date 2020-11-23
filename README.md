[![CircleCI](https://circleci.com/gh/silleknarf/craicbox.svg?style=shield)](https://circleci.com/gh/silleknarf/craicbox)

README
======

Craicbox is a collection of party games playable with a virtual room of your friends on a phone or computer.

There are two minigames so far:

**Art Master** - a drawing game where everyone has to rapidly create art for the other players to critique  
**Sentenced To Death** - a game where you fill in the gaps in each other's sentences for hilarious results

PLAY
====

[craicbox.app](https://craicbox.app)

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

Create a `.env` file in the root directory of the project and set the variables below:

    CRAICBOX_DATABASE_PASSWORD=<password_of_your_choosing>
    SOCKETIO_PASSWORD=<password_of_your_choosing>
    NEW_RELIC_MONITOR_MODE=false

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

To set up new relic (application performance monitoring), set the variables below in the `.env` file:

    NEW_RELIC_LICENSE_KEY=<your_new_relic_license_key>
    NEW_RELIC_MONITOR_MODE=true

Production Setup
================

1. Set up a kubernetes cluster which has got at least one persistent volume and node

1. Push the images for seed, service and UI up to an image registry

1. Add a secret for the image registry used  
`kubectl create secret docker-registry regcred --docker-server=rg.nl-ams.scw.cloud/craicbox --docker-username=nologin --docker-password=<your_password> --docker-email=<your_email> -n craicbox`

1. Add a secret called mysql-secrets with a value in data for the key: `mysql-root-password`

1. Add a secret called socketio-secrets with a value in data for the key: `socketio-password`

1. Add a secret called newrelic-secrets with a value in data for the key: `newrelic-password`

1. Update the k8s templates to point the registry images

1. Run in all the k8s templates
