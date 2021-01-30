# cquestionnaire
Build questionnaires

## Table of contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [License](#license)

## Requirements

  * Python 3.7.4
  * MySQL Community Server 5.7.12

## Installation

Install from the source:

```sh
$ git clone https://github.com/cjz25/cquestionnaire.git
```

Create a virtual environment:

```sh
$ cd cquestionnaire/
$ python3 -m venv env
$ source env/bin/activate
```

Activate the virtual environment:

```sh
$ source env/bin/activate
```

Note: For Windows
```sh
> .\env\Scripts\activate
```

Install requirements:

```sh
$ pip3 install -r requirements.txt
```

## Usage

### Set up your configuration file: my.cnf

Note: Please make sure you have created a database.

### Migrate

```sh
$ python3 manage.py migrate
```

### Run the server

```sh
$ python3 manage.py runserver
```

### You have the following APIs:

For questionnaires:
* GET: /api/questionnaires/
* POST: /api/questionnaires/
* GET: /api/questionnaires/<pk>/
* PUT: /api/questionnaires/<pk>/
* DELETE: /api/questionnaires/<pk>/

For questions with choices:
* GET: /questionnaires/<questionnaire_pk>/questions/
* POST: /questionnaires/<questionnaire_pk>/questions/
* GET: /questionnaires/<questionnaire_pk>/questions/<pk>/
* PUT: /questionnaires/<questionnaire_pk>/questions/<pk>/
* DELETE: /questionnaires/<questionnaire_pk>/questions/<pk>/

## License
MIT License
