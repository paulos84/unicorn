An application created for recording and reviewing data from trials on galacto-oligosaccharide production using an enzyme labelled 'white unicorn'.

It provides an API to allow the database to be queried as well as updated, To record data in the database, the application provides html forms for recording experiment details along with a field allowing csv files of results to be uploaded. The API allows the database to be queried and updated/edited. The API follows RESTful design principles, providing data in JSON format through endpoints detailed as follows....

...Charts

default endpoint: 127.0.0.1:8080/api/experiment

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


    python run.py runserver


API endpoints
-------------
