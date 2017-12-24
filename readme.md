An API for managing data from in-house trials of an enzyme-based process utilizing lactose to manufacture an ingredient in infant milk formula called galacto-oligosaccharides (GOS).

It is built using the Flask-Restless framework and SQL-Alchemy. Flask-WTF is used to generate HTML forms to simplify recording of experiment details along with csv files of results and analytical data. Basic HTTP authentication is used for protecting access.

Getting Started
---------------
**Prerequisites**

Python 3.4, pip, virtualenv

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

After ensuring correct settings within config.py, run the server:

    $ python api.py


**4. Submit and query data**

The API allows database access through HTTP methods as defined by individual endpoints. Entering data for new Experiment instances should be done using the HTML form which contains a field for uploading csv files of results.

Flask-Restless provides default URLs for accessing data (see https://flask-restless.readthedocs.io/en/stable/customizing.html#http-methods)

