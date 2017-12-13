An application created for recording and reviewing data from trials of biotechnology-based manufacturing processes for a novel food ingredient.

The Flask-Restless extension facilitates a JSON API for database models defined using Flask-SQLAlchemy. Flask-WTF is used to generate html forms to simplify recording of experimental details along with csv files of results and analytical data.

Highcharts, a JavaScript library for Python, enables experiment results to be plotted in order to enable comparison of various enzyme and conditions combinations.


Install
-------

Clone this repo to your local machine. In the top level directory, create a virtual environment:

    $ virtualenv flask-aws
    $ source flask-aws/bin/activate
    -see example http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html

Now install the required modules:
 
    $ pip install -r requirements.txt
    

Create and populate database
----------------------------



Configure and run the API
--------------------------


API endpoints
-------------
Flask-Restless provides default endpoints for accessing data (see https://flask-restless.readthedocs.io/en/stable/customizing.html#http-methods).
E.g. http://host:port/api/experiment lists details for each individual experiment (date, aims etc.) along with the details stored within parent model instances (enzyme used, reaction conditions set, results).


Models
------
Explain what models attr names correspond to e.g. procedure_notes

Provide example of csv results, and mention to account for glucose etc
- or have example on html page alongside the form