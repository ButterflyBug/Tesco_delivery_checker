# Tesco delivery checker

[![Build Status](https://travis-ci.org/ButterflyBug/Tesco_delivery_checker.svg?branch=master)](https://travis-ci.org/ButterflyBug/Tesco_delivery_checker)

- [Tesco delivery checker](#tesco-delivery-checker)
  - [Documentation](#documentation)
  - [Development](#development)
  - [Dependencies](#dependencies)
  - [Running the script](#running-the-script)
    - [Environment variables](#environment-variables)
  - [Tests](#tests)
    - [Update cassettes](#update-cassettes)
  - [Deployment](#deployment)
  - [Code style](#code-style)

## Documentation
[butterflybug.github.io/Tesco_delivery_checker](https://butterflybug.github.io/Tesco_delivery_checker/)

## Development
Recommended Python version `3.8.0`

## Dependencies
`$ pipenv install --dev`

## Running the script
The script `run_checker.py` requires proper environmental variables to be set up before its code is run. They are essential for that program so that it is able to successfully log into the website and obtain all needed information about available or unavailable slots.

### Environment variables


| Variable               | Description                                               | Default |
| ---------------------- | --------------------------------------------------------- | ------- |
| `$ TESCO_EMAIL`        | Login to your Tesco account                               |         |
| `$ TESCO_PASSWORD`     | Password to your Tesco account                            |         |
| `$ WAIT_TIME`          | How often `run_checker.py` is performed in seconds        | `3600`  |
| `$ SENDGRID_API_KEY`   | API key to your [SendGrid](https://sendgrid.com/) account |         |
| `$ EMAIL_NOTIFICATION` | Email address which notification should be sent on        |         |


## Tests
`$ pytest`

### Update cassettes
To record a new cassette needed to run tests, that invalid one should be deleted.
Once the file is removed, the newest version and updated content of the website can be recorded again.

`$ pytest --record-mode=all`

## Deployment
The whole project's deployment is prepared to be supported with [`dokku`](http://dokku.viewdocs.io/dokku/).
To correctly deploy the application to external server some steps need to be followed:

1. Set up `dokku` on remote server.
2. Add remote to your local repository:

   `git remote add [remote_name] dokku@[server_address]:[application_name]`

   i.e. `git remote add dokku@example.com:tesco`

3. Deploy with:

   `git push [remote_name] master` 

4. Make sure that [environment variables](#environment-variables) are set:

   `dokku config:set [application_name] VARIABLE_NAME=VALUE`


## Code style
This project follows [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide.

`$ python -m flake8`

`$ black`

Type annotation [PEP484](https://www.python.org/dev/peps/pep-0484/) with `Mypy`

`$ mypy [file_path]`


