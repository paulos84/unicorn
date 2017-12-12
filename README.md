An application created for recording and reviewing data from trials on galacto-oligosaccharide (GOS) production. GOS is produced from lactose using biotechnology and is marketed as a prebiotic food ingredient.

The Flask-Restless extension is used to generate a JSON API for database models defined using Flask-SQLAlchemy. Flask-WTF is used to generate html forms to enable experiment details to be recorded along with csv files of results and analytical data.

Highcharts, a JavaScript library for Python, enables experiment results to be plotted.



In[8]: e = ConditionsSet.query.first()
In[9]: e.lactose_concentration()
Out[9]: 64.16772554002542

In[11]: q.owner_conditions.lactose_concentration()
Out[11]: 64.16772554002542





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
Flask-Restless provides default endpoints for accessing data: 127.0.0.1:8080/api/{model}
E.g. 127.0.0.1:8080/api/experiment lists details for individual experiments (dates, aims etc.) along with information stored within parent model instances (enzyme used, reaction conditions set, results)


Models
------
Explain what models attr names correspond to e.g. procedure_notes

Provide example of csv results, and mention to account for glucose etc
- or have example on html page alongside the form