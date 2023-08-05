PixelForest DRF
===============

![PyPI version](https://badge.fury.io/py/pixelforest-drf.svg)
![Python versions](https://img.shields.io/pypi/pyversions/pixelforest-drf.svg)
![Django versions](https://img.shields.io/pypi/djversions/pixelforest-drf.svg?colorB=44b78b)

This repository host the code of the PixelForest DRF package.
This package will host most of the reusable applications/code we use on a project basis as the PixelForest Dev Team.

**Note** This package is under public licensing because we figured it might be useful for other as it is.

Current subpackages
====================
- **utils**: A subpackage with useful tools for Django applications. Not an application itself (but used as one for testing), no need to add it to your installed apps
- **countries**: A django application to handle some location data, based on 3 levels: Country, SubRegion and Region
- **companies**: A django application to handle companies structure, based on 4 levels: CompanyGroup, Company, Subsidiary and Service
- **users**: A django application to handle users
- **rest**: A collection of basic apis for the applications subpackages

Getting started
===============

Requirements
------------

The following requirements will need to be installed and configured

- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org)

Installation
------------

You can install the package using pip:
```bash
pip install pixelforest_drf
```

Add the wanted application(s) to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...,
    'rest_framework',  # necessary to use pixelforest_drf.rest
    'phonenumber_field',  # necessary to use pixelforest_drf.users
    'pixelforest_drf.companies',
    'pixelforest_drf.countries',
    'pixelforest_drf.users',
    ...,
)
```

If you use the pixelforest_drf.users subpackage, define the user in your settings:
```python
AUTH_USER_MODEL = "users.PFUser"
```

Run the included migrations:
```bash
python3 manage.py migrate
```

Rest Endpoints
--------------

Add the wanted URL patterns:
```python
from pixelforest_drf.rest import api_urls

urlpatterns = [
    ...,
    path('', include(api_urls)),
    ...,
]
```

Or, if you are not using all subpackages, you can nitpick:
```python
from pixelforest_drf.rest.countries import api_urls as countries_urls
from pixelforest_drf.rest.companies import api_urls as companies_urls
from pixelforest_drf.rest.users import api_urls as users_urls

urlpatterns = [
    ...,
    path('', include(countries_urls)),
    path('', include(companies_urls)),
    path('', include(users_urls)),
    ...,
]
```

Contributing
============

Guidelines
----------
Please contact the [PixelForest Dev Team](mailto:devteam@pixelforest.io) for any bug report or feature request.

Credit
------

- Countries
    - countries_objects.csv: Merge of the [Wikipedia ISO 3166-1 article](http://en.wikipedia.org/wiki/ISO_3166-1#Officially_assigned_code_elements), and data from the [UN Statistics site](https://unstats.un.org/unsd/methodology/m49/overview) for regions and sub-regions.
    Work inpired by [lukes ISO-3166 Github](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes) but redone to allow for MIT Licensing.
    - flags.zip: [Country Flags](https://github.com/hjnilsson/country-flags) - (Public Domain)

Contributors
------------

**Jean-Xavier Raynaud** - [email](mailto:jx@pixelforest.io) - Product Owner / System Architect / Developer

**Milo Parigi** - [email](mailto:milo@pixelforest.io) - Scrum Master / Developer

**Victor Duvernois** - [email](mailto:victornithorynque@pixelforest.io ) -  Developer
