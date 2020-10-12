# Cyb-Django-Assignment

Django Rest + SQLite3

## Prerequisites

Python 3.6+

pip

## Setup 

Create & activate a virtual environment:
```bash
$ python3 -m venv env
$ source "/env/bin/activate"
```

Install packages from [requirements.txt](requirements.txt)
```bash
(env) $ pip install -r requirements.txt
```


## Run

Run server:
```bash
(env) $ python manage.py runserver
```

## :key: User Credentials

| UserName | Password | Is SuperUser |
| --- | --- | --- | 
| admin | admin | Yes |
| anil | strong123 | No |
| tathya | strong123 | No |

## Run Test

```bash
(env) $ pytest
```