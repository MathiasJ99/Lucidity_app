GENERAL INTRO
--------------
This is a RESTful Web app that allows users to submit applications for trademarks.

front-end: boostrap, JS, HTML, CSS

back-end: sqlite, python, flask, sqlalchemy, stripe API



TESTING -- APP
-----------
1. Create .env file in main directory
1. Activate local env by:   venv/Scripts/activate 
2. Run app by doing:  python app.py server run --port=4242

TESTING -- PAYMENTS
-----------
to test payments - get stripe cli
1. go to powershell
1. run: stripe login 
2. run: stripe listen --forward-to localhost:4242/webhook

TODO
--------------
- send email confirmation after order to rob and customer -mathias
- customise with colour scheme and name - mathias
- input sanitisation -mathias
- encrypt tables -mathias 
- put in docker file (optional) -mathias
- COMMENT CODE
- buy hosting online 
- get domian name 
- upload docker file to hosting page
- get https certificate and add to website
- change priceids, env variables, url to offical ones

TODO EXTRA 
---------------
- add google analytics to site
- seo optimisation
- delete tag button
- make user accounts 


CHANGING DATABASE STRUCTURE
---------------------
flask db migrate -m "Initial migration"
flask db upgrade

