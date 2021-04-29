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
```
GET: /api/questionnaires/list?size=5&page=1
POST: /api/questionnaires/
GET: /api/questionnaires/<pk>/
PUT: /api/questionnaires/<pk>/
DELETE: /api/questionnaires/<pk>/
```

For questions with choices:
```
GET: /api/questionnaires/<questionnaire_pk>/questions/
POST: /api/questionnaires/<questionnaire_pk>/questions/
GET: /api/questionnaires/<questionnaire_pk>/questions/<pk>/
PUT: /api/questionnaires/<questionnaire_pk>/questions/<pk>/
DELETE: /api/questionnaires/<questionnaire_pk>/questions/<pk>/
```

For modifying the sequence of a question:
```
PUT: /api/questionnaires/<questionnaire_pk>/questions/<pk>/sequence/
```

## License
MIT License
