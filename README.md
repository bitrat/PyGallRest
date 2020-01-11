# Gallagher Mobile Credential – Self Service application

This application (set to run on localhost) consists of:

## Vue.js Front-end

simple-auth\ - where users can login, register and reset their password, in order to receive a mobile credential for a specified time (10 minutes – this time is adjustable)

## Flask Back-end

env\flask_app.py - this processes the user front-end requests and checks the users access group and whether they are an authorized user

## Gallagher Access Control system

REST API – cardholder licensable feature – updates authorized cardholder Personal Data Fields so they can be sent a mobile credential

# Getting Started

## Install and setup Gallagher
  
* create a REST client (= API key), enable REST port 8094, create cert thumbprint (*.pfx file), set client cert (pin it in Gallagher Server properties)

* create Access Group(s)
  - RequestAccess
  - NoAccess
* create PDFs
  - Email
  - Phone
  - VerifyPassword
  - ResetCode
  - ResetExpiry
* create Users
  - create at least 2 users in RequestAccess access group
  - create at least 2 users in NoAccess access group

## Install and setup Vue.js
Create simple-auth Project – axios to send front-end requests to Flask app
  
* Navigate into PyGallRest\simple-auth Project folder

* npm install

* npm run serve

The vue app currently will run on localhost:8090

## Install and setup Flask
  
* Navigate into PyGallRest\env Project folder - install requirements

* You will need to create and then populate your .env file (this is a text file with your secrets or other information you want to reference as a variable rather than repeat code - i.e. Gallagher API parent address, Gallagher API key, Email password etc) - the python-dotenv library is used to reference this file during app functioning.
  - GALLAGHER_API="https://127.0.0.1:8904/api"
  - CERT_FILENAME="XXX.pfx"
  - CERT_PSW="XXX"
  - HEADER_AUTH="XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX"   (this contains the Gallagher API Key)
  - MAIL_DEFAULT_SENDER="xxx@xxx.com"
  - MAIL_USERNAME="xxx@xxx.com"
  - MAIL_PASSWORD="XXX"
  
* .\\Scripts\activate

* python flask_app.py

The Flask app currently will run on localhost:5000

