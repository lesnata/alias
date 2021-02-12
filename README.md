## Table of contents
* [General info](#general-info)
* [Functionality](#functionality)
* [Technologies](#technologies)
* [Style conventions](#style-conventions)
* [Setup](#setup)
* [Running in shell](#running-in-shell)
* [Tests](#tests)

## General info
The app introduces an "Alias" object/model, defined as such:
- ``alias`` field - string (no specific requirements);
- ``target`` field - string (a "soft foreign key" to slugs of other models/apps 
    of the existing project; no more than 24 characters);
- ``start`` field - microsecond precision timestamp/datetime;
- ``end`` field - microsecond precision timestamp/datetime or None.


## Functionality
- referred_obj_slug() - gets list of slugs for particular alias.
        Limitation on particular end period is optional;
- get_aliases() - gets aliases which were running at the specific time.
        Aliases may start before ``from_time`` or end after ``to_time``;
- replace_alias() - replaces an existing alias with a new one
        at a specific time point.


## Technologies
Project is created with:
* Django==3.1.6
* black==20.8b1
* flake8==3.8.4
* coverage==5.4
* psycopg2-binary==2.8.6


## Style conventions
For code conventions used Black and Flake8 library. 
All functions and model methods have explicit doc strings explanations.


## Setup
To run this project locally, make the following:

```
$ git clone https://github.com/lesnata/alias.git
$ cd alias
$ virtualenv venv_alias
$ source venv_alias/bin/activate
$ (venv_alias)$ pip install -r requirements.txt
$ (venv_alias)$ python manage.py runserver
```

## Running in shell
To enter inside SQLite DB and check functionality please run:
```
$ python manage.py shell
>>> from app.models import Alias, Object;
>>> from app.views import get_aliases, referred_obj_slug, replace_alias;
>>> from datetime import datetime;
>>> 
>>> Alias.objects.values_list();
>>> Object.objects.values_list();
>>> 
>>> referred_obj_slug('a');
>>> 
>>> from_time = datetime.now();
>>> to_time = datetime.now();
>>> get_aliases(target='whatsapp', from_time=from_time, to_time=to_time);
>>> 
>>> replace_at = datetime.now();
>>> replace_alias(4, replace_at, 'Lumous');
```
Or you may enter as a user via admin panel:
```
default-user
Berlin-tomato-2
```

## Tests
* Tests are separated into distinct folder /tests/ with models and views tests. 
* Unit test coverage is 100%. 
* Checked with 'Coverage.py' lib:

```
Name                                        Stmts   Miss  Cover
---------------------------------------------------------------
app/__init__.py                                 0      0   100%
app/admin.py                                    3      0   100%
app/apps.py                                     3      0   100%
app/models.py                                  23      0   100%
app/tests/test_models.py                       24      0   100%
app/tests/test_views.py                        47      0   100%
app/views.py                                   33      0   100%
---------------------------------------------------------------
TOTAL                                         144      0   100%

```

To check tests run: 
```
python manage.py test ./app/tests/
```

