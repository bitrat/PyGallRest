# Gallagher Mobile Credential – Self Service application

This application (set to run on localhost) consists of:

## Vue.js Front-end

simple-auth folder - where users can login, register and reset their password, in order to receive a mobile credential for a specified time (10 minutes – this time is adjustable)

## Flask Back-end

flask_app.py - this processes the user front-end requests and checks the users access group and whether they are an authorized user

## Gallagher Access Control system

REST API – cardholder licensable feature – updates authorized cardholder Personal Data Fields so they can be sent a mobile credential

# Getting Started

## Install and setup Gallagher
  
* create a REST client (= API key), enable REST port 8094, create cert thumbprint, set client cert (pin it)

* create Access Group(s), PDFs, Users

## Install and setup Vue.js
Create simple-auth Project – axios to send front-end requests to Flask app
  
* Navigate into PyGallRest\simple-auth Project folder

* npm install

* npm run serve

The vue app currently will run on localhost:8090

## Install and setup Flask
  
* Navigate into PyGallRest\env Project folder - install requirements
  
* .\\env\Scripts\activate

* python flask_app.py

The Flask app currently will run on localhost:5000

