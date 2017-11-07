An application to create and manage a database for recording data relating to enzyme reaction trials.  


It provides an API to allow the database to be queried as well as updated, in addition to html forms and csv file upload or experiment results. The API follows REST design principles, providing data in JSON format through endpoints detailed as follows.

...Charts

Clone this repo to your local machine. In the top level directory, create a virtual environment:

    $ virtualenv flask-aws
    $ source flask-aws/bin/activate

Now install the required modules:
 
    $ pip install -r requirements.txt
    

Create and populate database
----------------------------



Configure and run the API
--------------------------


    python run.py runserver


API endpoints
-------------
