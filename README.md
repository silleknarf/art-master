[![CircleCI](https://circleci.com/gh/silleknarf/craicbox.svg?style=shield)](https://circleci.com/gh/silleknarf/craicbox)
# README

Craicbox is a collection of party games playable with a virtual room of your friends on a phone or computer.

There are two minigames so far:

**Art Master** - a drawing game where everyone has to rapidly create art for the other players to critique  
**Sentenced To Death** - a game where you fill in the gaps in each other's sentences for hilarious results

## Play it now
[📦 craicbox.app](https://craicbox.app)

## Contributing
Development in progress!
[Trello TODO Board](https://trello.com/b/xC2SMsIk/craicbox)
Contributions are welcome, please feel free to submit a PR.

## Architecture

The users of the game primarily interact with an HTML5 website. The website is a Single Page App which interacts with an API service. The API service depends on a MySQL database. There is also a celery worker which runs background tasks and it uses a redis cache to store state.

**ui**
The UI is a mobile-first cross-browser HTML5 app written in React and Redux. 

**service** 
The backend provides the API and is responsible for the business logic. It is written in Python using the flask web service framework. It is stateless and horizontally scalable.

**db**
There is a one node MySQL database which stores the state for all games and users.

**celery**
There are Python celery workers. They store long-running tasks in a redis cache and they perform background work. We use celery tasks to manage the lifecycle of timed game rounds.

## Getting Started

1. Get the code:
    `git clone https://github.com/silleknarf/craicbox.git`

1. Install Docker

1. Create a `.env` file in the root directory of the project and set the variables below:
    ```
    CRAICBOX_DATABASE_PASSWORD=<password_of_your_choosing>
    SOCKETIO_PASSWORD=<password_of_your_choosing>
    NEW_RELIC_MONITOR_MODE=false
    ```

 1. Seed the `craicbox` database:
    `docker-compose up -d --build seed`

1. Start the db, service and UI:
    ```
    docker-compose up -d --build ui
    Open browser with url: http://localhost:3000
    ```

## How To Guides

To update the data model:

    docker-compose up -d --build generate_data_model

To run the service tests:

    docker-compose up --build service_tests

Run Storybook:

    docker-compose up -d --build storybook
    Open browser with url: http://localhost:9009

To set up new relic (application performance monitoring), set the variables below in the `.env` file:

    NEW_RELIC_LICENSE_KEY=<your_new_relic_license_key>
    NEW_RELIC_MONITOR_MODE=true


## Production Setup

1. Set up a kubernetes cluster which has got at least one persistent volume and node

1. Push the images for seed, service and UI up to an image registry

1. Add a secret for the image registry used  
`kubectl create secret docker-registry regcred --docker-server=<your_registry> --docker-username=nologin --docker-password=<your_password> --docker-email=<your_email> -n craicbox`

1. Add a secret called mysql-secrets with a value in data for the key: `mysql-root-password`

1. Add a secret called socketio-secrets with a value in data for the key: `socketio-password`

1. Add a secret called newrelic-secrets with a value in data for the key: `newrelic-password`

1. Update the k8s templates to point the registry images

1. Run in all the k8s templates
