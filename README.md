An application created for recording and reviewing data from trials of biotechnology-based manufacturing processes for a novel food ingredient.

The Flask-Restless extension facilitates a JSON API for database models defined using Flask-SQLAlchemy.

Flask-WTF is used to generate html forms to simplify recording of experimental details along with csv files of results and analytical data.

Highcharts, a JavaScript library for Python, enables experiment results to be plotted in order to enable comparison of various enzyme and conditions combinations.

Getting Started
---------------
**Prerequisites**

Python 3.4

pip

virtualenv

**1. Clone or copy repository**

**2. Set up Virtual Environment**

Create a virtual environment named aurn-venv:

    $ virtualenv unicorn-venv

Activate the virtual environment:

    $ source unicorn-venv/bin/activate
    (unicorn-venv) $

Use *pip* to install requirements:

    (unicorn-venv) $ pip install requirements.txt

Verify that packages have been installed:

    (unicorn-venv) $ pip freeze
    Flask==0.12
    Flask_Restless==0.17.0
    Flask_SQLAlchemy==2.1
    Flask_WTF==0.14.2
    pandas==0.20.1
    Werkzeug==0.11.15
    WTForms==2.1

**3. Configure and run the API**

After ensuring correct settings within config.py, the database can be queried and updated after running the server:

    $ python api.py

API endpoints
--------------
Flask-Restless provides default endpoints for accessing data (see https://flask-restless.readthedocs.io/en/stable/customizing.html#http-methods)

Trial data entry form
---------------------

