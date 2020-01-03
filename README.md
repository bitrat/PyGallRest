<h1>Gallagher Mobile Credential – Self Service application<h1>

This application consists of a:

* Vue.js Front-end – where users can login, register and reset their password, in order to receive a mobile credential for a specified time (10 minutes – this time is adjustable)
* Flask Back-end – this processes the user front-end requests and checks the users access group and whether they are an authorized user
* Gallagher Access Control system - REST API – cardholder licensable feature – updates authorized cardholder Personal Data Fields so they can be sent a mobile credential

<h2>Getting Started<h2>

<h3>Install and setup Gallagher<h3> 
* create a REST client (= API key), enable REST port 8094, create cert thumbprint, set client cert (pin it)
* create Access Group(s), PDFs, Users

<h3>Install and setup Vue.js<h3>
Create simple-auth Project – axios to send front-end requests to Flask app
* Navigate into PyGallRest\simple-auth Project folder
* npm install
* npm run serve
The vue app currently will run on localhost:8090

<h3>Install and setup Flask<h3>
* Navigate into PyGallRest\env Project folder
* .\\env\Scripts\activate
* python flask_app.py
The Flask app currently will run on localhost:5000

