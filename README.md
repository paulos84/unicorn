An application created for recording and reviewing data from trials on galacto-oligosaccharide (GOS) production using various enzyme. GOS is marketed as a prebiotic food ingredient, predominantly used in infant milk formulas (further reading: http://onlinelibrary.wiley.com/doi/10.1111/j.1541-4337.2010.00119.x/full).

It uses the Flask-Restless extension to generate a JSON API for database models defined using Flask-SQLAlchemy to allow the database to be queried as well as updated, To record data in the database, the application provides html forms for recording experiment details along with a field allowing csv files of results to be uploaded. The API allows the database to be queried and updated/edited. The API follows RESTful design principles, providing data in JSON format through endpoints detailed as follows....

...Charts



In[8]: e = ConditionsSet.query.first()
In[9]: e.lactose_concentration()
Out[9]: 64.16772554002542

In[11]: q.owner_conditions.lactose_concentration()
Out[11]: 64.16772554002542



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


API endpoints
-------------


Models
------
Explain what models attr names correspond to e.g. procedure_notes

Provide example of csv results, and mention to account for glucose etc
- or have example on html page alongside the form