# Aidoo

[![Coverage](https://github.com/o-brand/golf/actions/workflows/test_coverage.yml/badge.svg)](https://github.com/o-brand/golf/actions/workflows/test_coverage.yml)
[![Django Tests](https://github.com/o-brand/golf/actions/workflows/django-tests.yml/badge.svg)](https://github.com/o-brand/golf/actions/workflows/django-tests.yml)

Aidoo is an online volunteering platform designed to empower communities. We connect volunteers with aid positions and local businesses in their community.

## How to get started

### How to build the code
In order to build and run the code a few Python modules must be installed first. We recommend using Python 3.10, and the list of modules and versions can be found in the requirements.txt file in the directory. These can be installed using pip. (Sometimes installing psycopg2 gives an error. If this happens, install the requirements from requirements-dev.txt)

After installing all the required packages, the code can be run by executing the command ```python manage.py runserver``` or ```python3 manage.py runserver``` from within the Aidoo folder. This will provide a local web address for you to view the app in your browser.

Alternatively, a deployed version of the code is available online at https://aidoo.herokuapp.com/. For an *optimal* experience we recommend viewing the website on Chrome.

### How to test the code
Assuming the software requirements have been satisfied as above, you can run our unit tests using the command ```python manage.py test``` or ```python3 manage.py test``` from within the Aidoo folder.
