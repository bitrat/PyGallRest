from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import json
import bcrypt
import pendulum
import os
from os.path import join, dirname
from requests_pkcs12 import get
from requests_pkcs12 import patch
from requests_pkcs12 import post
from dotenv import load_dotenv
from random import *
from flask import request
from flask import abort
import requests
from flask_mail import Mail, Message
from flask import url_for
import uuid

# ENV variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
api_url_base = os.getenv("GALLAGHER_API")
cert_filename = os.getenv("CERT_FILENAME")
cert_password = os.getenv("CERT_PSW")
cert_server = os.getenv("CERT_SERVER")
auth_header_key = os.getenv("HEADER_AUTH")
auth_key = "GGL-API-KEY "+auth_header_key
mail_user = os.getenv("MAIL_USERNAME")
mail_sender = os.getenv("MAIL_DEFAULT_SENDER")
mail_psw = os.getenv("MAIL_PASSWORD")

# Request headers
headers = {
    'Authorization': auth_key,
    'Content-Type':'application/json'
}

# Gallagher varaibles
AllowedAccessGroup = "RequestAccess"

# configuration
DEBUG = True

# instantiate the flask app
app = Flask(__name__)
app.config.from_object(__name__)

# mail server settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = mail_user
app.config['MAIL_DEFAULT_SENDER'] = mail_sender 
app.config['MAIL_PASSWORD'] = mail_psw

mail = Mail(app)

#------------ START of API functions to Gallagher -----------------
# Set base path for each request
def _url(path):
    return 'https://127.0.0.1:8904/api'+path

def get_all_info():
    return get(_url('/'), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

# NOTE: get = requests-pkcs get request
def get_all_info():
    return get(_url('/'), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def get_accessgroups():
    return get(_url('/access_groups'), verify=False, headers=headers, pkcs12_filename=cert_filename, pkcs12_password=cert_password)

def get_accessgroup_cardholders(AG_cardholders_URL):
    return get(_url(AG_cardholders_URL), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def get_specific_accessgroup(id):
    id_string = str(id)
    return get(_url('/access_groups/'+id_string), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def get_cardholders():
    return get(_url('/cardholders'), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def get_cardholder_details(cardholder_URL):
    return get(cardholder_URL, pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def get_specific_cardholders(id):
    id_string = str(id)
    return get(_url('/cardholders/'+id_string), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def get_cardholder_pdf_list():
    return get(_url('/personal_data_fields'), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

#def get_pdf_content(get_pdf_content):
 #   return get(get_pdf_content, pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def get_cardtypes():
    return get(_url('/card_types'), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def assign_cardtype():
    return get(_url('/card_types/assign'), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def get_cardtype(name):
    return get(_url('/card_types/assign?name='+name), pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)

def update_cardholder_pdf(cardholder_href, json_input):
    print(cardholder_href)
    print(json_input)
    return patch(cardholder_href, json = json_input, pkcs12_filename=cert_filename, pkcs12_password=cert_password, verify=False, headers=headers)
#------------ END of API fucntions to Gallagher ----------------

#------------ Start GENERAL FUNCTIONS --------------------------
def create_resetpsw_key():    
    return str(uuid.uuid4())

def send_reset_msg(key,mail_rcp):    
    with app.app_context():
        msg = Message(subject="Request Access - Password Reset", sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[mail_rcp])
        msg.body="Please go to this URL to reset your password: http://localhost:8090/change-password/"+str(key)       
        mail.send(msg)

def set_reset_expiry(from_date):
    # NZDST +13 hours (if before 1 pm, then with add 24 hours, ResetDate is programmed as today 00:00, not time and date
    until_reset = from_date.add(hours=48)
    print(until_reset)
    # To enable datetime to be serialized
    untilReset = until_reset.isoformat()
    return untilReset

def set_mobile_expiry(from_date):
    until_reset = from_date.add(minutes=10)
    print(until_reset)
    # To enable datetime to be serialized
    untilReset = until_reset.isoformat()
    return untilReset

def error_status(error_msg):
    error_message = "----------------------------------------------\nERROR: "+error_msg+"\n----------------------------------------------"
    return error_message
#------------ End GENERAL FUNCTIONS --------------------------

# ----------- Start - PASSWORD Functions -----------------------
def create_password(verifypass):
    # Hash + Salt password with bcrypt
    # Default rounds are 12
    salt = bcrypt.gensalt(rounds=16)
    hashed = bcrypt.hashpw(verifypass.encode('utf-8'), salt)
    print(salt)
    print(hashed)
    hashed_text = hashed.decode('utf-8')
    return hashed_text

def convert_password(update_data):
    # convert python dict to JSON string
    text_patch_password = json.dumps(update_data)
    # convert JSON string to python object
    json_patch_password = json.loads(text_patch_password)
    return json_patch_password

def verify_password(input_to_hash,hashedpass):
    # Verify password with "VerifyPassword" PDF
    print(input_to_hash.encode('utf-8'))
    print(hashedpass.encode('utf-8'))
    if (bcrypt.hashpw(input_to_hash.encode('utf-8'), hashedpass.encode('utf-8')) == hashedpass.encode('utf-8')): 
        print("Password matched - user verified")
        return True
    else:    
        print("Password does not match - user not valid")
        return False
# ----------- End - PASSWORD Functions -----------------------

# ----------- Start - FLASK ROUTES ----------------------------
# CORS Implementation
# - enable CORS
# - restrict Origin
CORS(app, resources={r"/*": {"origins": "http://localhost:8090"}})
# TESTING ONLY: cors = CORS(app) # This makes the CORS feature cover all routes in the app
# EXAMPLE: @app.route('/routeToUse', methods=['POST'])
# EXAMPLE: @cross_origin(origin='localhost',headers=headers)

@app.route('/postLogin', methods=['GET','POST'])
# TESTING ONLY: @cross_origin(origin='*')
@cross_origin(origin='localhost',headers=headers)
def post_LoginData():
    if request.method == "GET":
        return jsonify('This is a POST route only')
        # Below line requires Internet
        #url = 'https://dog.ceo/api/breeds/list/all'
        # For https - you need to have cert sorted, or ignore cert NOT RECOMMENDED 
        #response = requests.get(url, verify=False)  
    elif request.method == "POST":
        user_data = request.get_json()
        #print(user_data)
        #user_email = request.json.get('email')
        #user_password = request.json.get('password')
        #return jsonify(user_email, user_password)
        #return jsonify(auth_header_key)

        user_count = 0
        print('----- START LOGIN Script ---------------------------')
        # INPUT from Cardholder - FORM
        WNemail = request.json.get('email')
        WNVerify = request.json.get('password')  

        if (WNemail and WNVerify):
            ag_list = get_accessgroups()
            data_ag_list = ag_list.json()
            print('                                              ')
            print('----------------------------------------------')
            for each in data_ag_list['results']:   
                #print(each['name'])
                if (each['name'] == "RequestAccess"):
                    AG_id = each['id']
                    # get cardholders from the specific Access group
                    AG_cardholders_URL = "/access_groups/"+AG_id+"/cardholders"
                    AG_cardholders = get_accessgroup_cardholders(AG_cardholders_URL)
                    #print('----------------------------------------------')
                    #print(AG_cardholders.json())
                    data_AG_cardholders = AG_cardholders.json()
                    # Foreach cardholder in the Access group get their details URL
                    #print('----------------------------------------------')
                    for cardholder in data_AG_cardholders['cardholders']:
                        #print('---------------HREF---------------------------')
                        CH_href = cardholder['cardholder']['href']
                        print(CH_href)
                        #print('----------------------------------------------')
                        cardholder_details = get_cardholder_details(CH_href)
                        data_cardholder_details = cardholder_details.json()
                        #print(data_cardholder_details)
                        #print(json.dumps(data_cardholder_details, indent=4))
                        extract_data_cardholder_details = json.dumps(data_cardholder_details, indent=4)
                        #print(extract_data_cardholder_details)
                        #print('----------------------------------------------')                    
                        # compare Email to the one entered
                        # make sure the cardholder access group membership is still active
                        data_CH_detail = json.loads(extract_data_cardholder_details)
                        if ((data_CH_detail['@Email'] == WNemail) and (data_CH_detail['accessGroups'][0]['status']['type'] == 'active')): 
                            print('----------------------------------------------')
                            print(data_CH_detail['@Email'])
                            # TO DO: change 'Phone' to 'Mobile' or 'Cellphone'
                            print(data_CH_detail['@Phone'])

                            # Test if VerifyPassword PDF exists
                            if ('@VerifyPassword' in data_CH_detail):
                                print('----------------------------------------------') 
                                # Verify password entered by user with hashed bcrypt value 
                                if (verify_password(WNVerify,data_CH_detail['@VerifyPassword'])):
                                    # password verified
                                    print('-------- GET "Mobile Credential" CARD TYPE DETAILS -----------')
                                    get_mc = get_cardtype("Mobile Credential")
                                    data_mc = get_mc.json()
                                    #print(data_mc)
                                    #print('----------------------------------------------')
                                    for each_mc in data_mc['results']:   
                                        #print(each_mc['name'])
                                        #print(each_mc['id'])
                                        credential_href = each_mc['href']
                                        print(credential_href)
                                        if (each_mc['credentialClass'] == 'mobile'):
                                            #print(each_mc['credentialClass'])
                                            # TO DO: Define Timezone of destination
                                            from_date = pendulum.now()
                                            print(from_date)
                                            # To enable datetime to be serialized
                                            fromDate = from_date.isoformat()
                                            untilDate = set_mobile_expiry(from_date)
                                            text_credential_assign = json.dumps({"href": CH_href,"cards": {"add": [{"type": {"href": credential_href},"status": {"value": "Active"},"invitation": {"email": data_CH_detail['@Email'],"mobile": data_CH_detail['@Phone']},"from": fromDate,"until": untilDate,"credentialClass": "mobile"}]}})                                
                                            # convert JSON string to python object
                                            json_credential_assign = json.loads(text_credential_assign)
                                            patch_mc_date = update_cardholder_pdf(CH_href, json_credential_assign)
                                            if patch_mc_date.status_code == 204:
                                                user_count+=1
                                                print('----------------------------------------------') 
                                                print(" Mobile Credential successfully assigned to "+data_CH_detail['@Email'])
                                                print('----------------------------------------------') 
                                                success_msg = "LOGIN SUCCESSFUL - Mobile Credential successfully assigned to "+data_CH_detail['@Email']
                                                #success_msg = data_CH_detail['@Email']
                                                success_code = 200
                                                return(success_msg, success_code)
                                else:
                                    user_count=0
                                    error_notify = error_status("Password could not be verified - Please try again")
                                    print(error_notify)
                            else:
                                user_count=0
                                error_notify = error_status("User is Not Registered yet - Register to set Password")
                                print(error_notify)
                        else:
                            user_count=0
                            error_notify = error_status("Cardholder not valid")
                            print(error_notify)
        else:
            user_count=0
            error_notify = error_status("Email and/pr password is Empty")
            print(error_notify)
        
        if (user_count == 0):  
            msg = "LOGIN FAILED - User not Verified - Email and/or Password is wrong OR Have you not registered yet ?"
            code = 400       
            return msg, code
        
        print('----- END LOGIN Script ---------------------------')
 
@app.route('/postRegister', methods=['GET','POST'])
#@cross_origin(origin='*')
@cross_origin(origin='localhost',headers=headers)
def post_RegisterData():
    if request.method == "GET":
        return jsonify('This is a POST route only')
        # Below line requires Internet
        #url = 'https://dog.ceo/api/breeds/list/all' 
        #response = requests.get(url, verify=False) 
        
        # For https - you need to have cert sorted, or ignore cert NOT RECOMMENDED 
        #all_hrefs = get_all_info()
        #return(all_hrefs.json())
    elif request.method == "POST":       
        # CHECK for no users with the correct email address
        user_count = 0
        print('----- START Script ---------------------------')
        # Ask for Cardholder details
        WNemail = request.json.get('email')
        print(WNemail)
        WNVerify = request.json.get('password')
        #print(WNVerify)
        WNComparePassword = request.json.get('verifyPassword')
        #print(WNComparePassword)

        if (WNemail and WNVerify and WNComparePassword):
            if (WNVerify == WNComparePassword):
                # Check the specified Access Group
                ag_list = get_accessgroups()
                #print(ag_list.json())
                data_ag_list = ag_list.json()

                for each in data_ag_list['results']:   
                    #print(each['name'])
                    if (each['name'] == "RequestAccess"):
                        AG_id = each['id']
                        #print(AG_id)
                        # get cardholders from the specific Access group
                        AG_cardholders_URL = "/access_groups/"+AG_id+"/cardholders"
                        #print(AG_cardholders_URL)
                        AG_cardholders = get_accessgroup_cardholders(AG_cardholders_URL)
                        #print('----------------------------------------------')
                        #print(AG_cardholders.json())
                        data_AG_cardholders = AG_cardholders.json()
                        # Foreach cardholder in the Access group get their details URL
                        #print('----------------------------------------------')
                        for cardholder in data_AG_cardholders['cardholders']:
                            CH_href = cardholder['cardholder']['href']
                            print(CH_href)
                            #print('----------------------------------------------')
                            cardholder_details = get_cardholder_details(CH_href)
                            data_cardholder_details = cardholder_details.json()
                            #print(data_cardholder_details)
                            #print(json.dumps(data_cardholder_details, indent=4))
                            extract_data_cardholder_details = json.dumps(data_cardholder_details, indent=4)
                            #print(extract_data_cardholder_details)
                            data_CH_detail = json.loads(extract_data_cardholder_details)
                            if ((data_CH_detail['@Email'] == WNemail) and (data_CH_detail['accessGroups'][0]['status']['type'] == 'active')): 
                                print('----------------------------------------------')
                                print(data_CH_detail['@Email'])
                                print(data_CH_detail['@Phone'])
                                # Test if VerifyPassword PDF exists
                                if ('@VerifyPassword' in data_CH_detail):
                                    user_count=0
                                    error_notify = error_status("User is already registered")
                                    print(error_notify)
                                else:                             
                                    # Password does not already exists in VerifyPassword PDF
                                    hash_text = create_password(WNVerify)
                                    data_update = {'personalDataDefinitions': [{'@VerifyPassword': {'value': hash_text}}]} 
                                    hash_json_patch_password = convert_password(data_update)
                    
                                    success_pass_write = update_cardholder_pdf(CH_href, hash_json_patch_password)
                                    if success_pass_write.status_code == 204:
                                        user_count+=1
                                        msg = "REGISTRATION was SUCCESSFUL - Please LOGIN with the email and password you just entered, to receive your mobile credential."
                                        code = 200       
                                        return msg, code
                                        print("SUCCESS: Password written to VerifyPassword PDF")                               
                                print('----------------------------------------------')
                            else:
                                user_count=0
                                error_notify = error_status("Cardholder not valid")
                                print(error_notify)
            else:
                user_count=0
                error_notify = error_status("Passwords didn't match")
                print(error_notify)
                    
        else:
            user_count=0
            error_notify = error_status("Email and/pr password is Empty")
            print(error_notify)

        if (user_count == 0):  
            msg = "REGISTRATION FAILED - Registered in the Past Already ? - OR - You are Not Authorized to Register"
            code = 400       
            return msg, code    
        print('----- END Register Script ---------------------------')

@app.route('/rqForgotPassword', methods=['POST'])
#@cross_origin(origin='*')
@cross_origin(origin='localhost',headers=headers)
def post_rqForgotPassword(): 
    if request.method == "POST":  
        # Get user's email address and check if a reset password is allowed
        user_count = 0
        print('----- START FORGOT PASSWORD Script ---------------------------')
        # Cardholder Input - FORM
        WNemail = request.json.get('email')

        if (WNemail):
            # Check the specified Access Group
            ag_list = get_accessgroups()
            print(ag_list.json())
            data_ag_list = ag_list.json()
            print('                                              ')
            print('----------------------------------------------')
            for each in data_ag_list['results']:   
                if (each['name'] == "RequestAccess"):
                    AG_id = each['id']
                    # get cardholders from the specific Access group
                    AG_cardholders_URL = "/access_groups/"+AG_id+"/cardholders"
                    AG_cardholders = get_accessgroup_cardholders(AG_cardholders_URL)
                    data_AG_cardholders = AG_cardholders.json()
                    # Foreach cardholder in the Access group get their details URL
                    for cardholder in data_AG_cardholders['cardholders']:
                        CH_href = cardholder['cardholder']['href']
                        #print(CH_href)
                        cardholder_details = get_cardholder_details(CH_href)
                        data_cardholder_details = cardholder_details.json()
                        extract_data_cardholder_details = json.dumps(data_cardholder_details, indent=4)
                        # compare Email to the one entered
                        # make sure the cardholder access group membership is still active
                        data_CH_detail = json.loads(extract_data_cardholder_details)
                        if ((data_CH_detail['@Email'] == WNemail) and (data_CH_detail['accessGroups'][0]['status']['type'] == 'active')): 
                            print('----------------------------------------------')
                            print(data_CH_detail['@Email'])
                            # TO DO: change 'Phone' to 'Mobile' or 'Cellphone'
                            print(data_CH_detail['@Phone'])
                            # resetCode date comparison
                            from_reset = pendulum.now()
                            # To enable datetime to be serialized
                            fromReset = from_reset.isoformat()
                            #print("From Date: ",fromReset)
                            #print(data_CH_detail)
        
                            # If ResetCode PDF is set and is not expired
                            if ('@ResetCode' in data_CH_detail):
                                if ('@ResetExpiry' in data_CH_detail):
                                    # Is ResetCode Expired ? No
                                    if (data_CH_detail['@ResetExpiry'] > str(fromReset)):
                                        user_count+=1
                                        # TO DO: TEST - Sending currently active Reset URL to user
                                        key_id = data_CH_detail['@ResetCode']
                                        rcp = data_CH_detail['@Email']
                                        try:
                                            #send_reset_msg(key_id,rcp)
                                            print('----------------------------------------------')
                                            print("SUCCESS: Reset Code sent to User")
                                            print('----------------------------------------------')
                                            success_msg = "PASSWORD RESET Code sent - Check your email and follow the Password Reset Link we sent you."
                                            success_code = 200
                                            return(success_msg, success_code)        
                                        except:
                                            user_count=0
                                            error_notify = error_status("Reset Email could not be sent")
                                            print(error_notify)
                                    # Is ResetCode Expired ? Yes
                                    else:
                                        untilResetDate = set_reset_expiry(from_reset)
                                        # Create new ResetCode
                                        reset_key = create_resetpsw_key()
                                        # Write new Expiry and ResetCode into cardholder PDF
                                        text_resetcode_assign = json.dumps({"@ResetCode": reset_key,"@ResetExpiry": untilResetDate})
                                        json_resetcode_assign = json.loads(text_resetcode_assign)
                                        patch_mc_date = update_cardholder_pdf(CH_href, json_resetcode_assign)
                                        if patch_mc_date.status_code == 204:
                                            user_count+=1
                                            # TO DO: Send "Reset URL" to user
                                            print('----------------------------------------------') 
                                            print(" Reset Code set and sent to "+data_CH_detail['@Email'])
                                            print('----------------------------------------------') 
                                            
                                            success_msg = "PASSWORD RESET successful - Check your email and follow the Password Reset Link we sent you."
                                            #success_msg = data_CH_detail['@Email']
                                            success_code = 200
                                            return(success_msg, success_code)                               
                                # If Reset Expiry is empty - put in an Expiry date and send a new Reset code
                                else:
                                    untilResetDate = set_reset_expiry(from_reset)
                                    # Create new ResetCode
                                    reset_key = create_resetpsw_key()
                                    # Write new Expiry and ResetCode into cardholder PDF
                                    text_resetcode_assign = json.dumps({"@ResetCode": reset_key,"@ResetExpiry": untilResetDate})
                                    json_resetcode_assign = json.loads(text_resetcode_assign)
                                    patch_mc_date = update_cardholder_pdf(CH_href, json_resetcode_assign)
                                    if patch_mc_date.status_code == 204:
                                        user_count+=1
                                        # TO DO: Send "Reset URL" to user
                                        print('----------------------------------------------') 
                                        print(" Reset Code set and sent to "+data_CH_detail['@Email'])
                                        print('----------------------------------------------') 
                                        
                                        success_msg = "PASSWORD RESET successful - Check your email and follow the Password Reset Link we sent you."
                                        #success_msg = data_CH_detail['@Email']
                                        success_code = 200
                                        return(success_msg, success_code)                                                           
                            else:                             
                                # Reset Code does not already exist in ResetCode PDF 
                                untilResetDate = set_reset_expiry(from_reset)
                                # Create ResetCode
                                reset_key = create_resetpsw_key()
                                # Write Expiry and ResetCode into cardholder PDF
                                text_resetcode_assign = json.dumps({"@ResetCode": reset_key,"@ResetExpiry": untilResetDate})
                                json_resetcode_assign = json.loads(text_resetcode_assign)
                                patch_mc_date = update_cardholder_pdf(CH_href, json_resetcode_assign)
                                if patch_mc_date.status_code == 204:
                                    user_count+=1
                                    # TO DO: TEST - Sending "Reset URL" to user
                                    key_id = reset_key
                                    rcp = data_CH_detail['@Email']
                                    try:
                                        #send_reset_msg(key_id,rcp)
                                        print('----------------------------------------------') 
                                        print(" Reset Expiry Date set and Reset Code sent to "+data_CH_detail['@Email'])
                                        print('----------------------------------------------') 
                                        success_msg = "PASSWORD RESET successful - Check your email and follow the Password Reset Link we sent you."
                                        success_code = 200
                                        return(success_msg, success_code)        
                                    except:
                                        user_count=0
                                        error_notify = error_status("Reset Email could not be sent")
                                        print(error_notify)                              
                        else:
                            user_count=0
                            error_notify = error_status("Cardholder not valid")
                            print(error_notify)

        else:
            user_count=0
            error_notify = error_status("Email and/pr password is Empty")
            print(error_notify)
                    
        if (user_count == 0):  
            msg = "RESET PASSWORD FAILED - You are Not Authorized"
            code = 400       
            return msg, code

        print('----- END FORGOT PASSWORD Script ---------------------------')

@app.route("/change-password/<id>", methods=['POST'])
#@cross_origin(origin='*')
@cross_origin(origin='localhost',headers=headers)
def changePassword(id):     
    if request.method == "POST":
        #return jsonify('Change Password POST route is: '+id)
        
        # Check user email is valid and in correct Access Group
        # Then check verification "RestCode" code is valid
        # If valid - reset the user's password to the one entered by the User
        user_count = 0
        print('----- START RESET PASSWORD Script ---------------------------')
        # Ask for Cardholder details
        WNemail = request.json.get('email')
        print(WNemail)
        WNVerify = request.json.get('password')
        #print(WNVerify)
        WNComparePassword = request.json.get('verifyPassword')
        #print(WNComparePassword)

        if (WNemail and WNVerify and WNComparePassword):
            if (WNVerify == WNComparePassword):
                # Check the specified Access Group
                ag_list = get_accessgroups()
                print(ag_list.json())
                data_ag_list = ag_list.json()
                print('                                              ')
                print('----------------------------------------------')
                for each in data_ag_list['results']:   
                    if (each['name'] == "RequestAccess"):
                        AG_id = each['id']
                        AG_cardholders_URL = "/access_groups/"+AG_id+"/cardholders"
                        AG_cardholders = get_accessgroup_cardholders(AG_cardholders_URL)
                        data_AG_cardholders = AG_cardholders.json()
                        for cardholder in data_AG_cardholders['cardholders']:
                            CH_href = cardholder['cardholder']['href']
                            #print(CH_href)
                            cardholder_details = get_cardholder_details(CH_href)
                            data_cardholder_details = cardholder_details.json()
                            extract_data_cardholder_details = json.dumps(data_cardholder_details, indent=4)
                            data_CH_detail = json.loads(extract_data_cardholder_details)

                            if ((data_CH_detail['@Email'] == WNemail) and (data_CH_detail['accessGroups'][0]['status']['type'] == 'active')): 
                                print('----------------------------------------------')
                                print(data_CH_detail['@Email'])
                                print(data_CH_detail['@Phone'])
                                from_reset = pendulum.now()
                                # To enable datetime to be serialized
                                fromReset = from_reset.isoformat()

                                # Test if Token is Valid PDF exists
                                if ('@ResetCode' in data_CH_detail):
                                    if (data_CH_detail['@ResetCode'] == id):
                                        if (data_CH_detail['@ResetExpiry'] > str(fromReset)):
                                            # Reset Token is valid and not expired
                                            hash_text = create_password(WNVerify)
                                            data_update = {'personalDataDefinitions': [{'@VerifyPassword': {'value': hash_text}, '@ResetCode': {'value': ""}, '@ResetExpiry': {'value': ""}}]}
                                            hash_json_patch_password = convert_password(data_update)
                                            # write the first hashed+salted password that user put in to that PDF
                                            success_pass_write = update_cardholder_pdf(CH_href, hash_json_patch_password)
                                            if success_pass_write.status_code == 204:
                                                user_count+=1
                                                msg = "PASSWORD RESET was SUCCESSFUL - Please LOGIN with the email and password you just entered, to receive your mobile credential."
                                                code = 200       
                                                return msg, code
                                                print("SUCCESS: New Password written to VerifyPassword PDF") 
                                            else:
                                                user_count=0
                                                error_notify = error_status("Could not update User - No new Password saved")
                                                print(error_notify)
                                        # If Reset Expiry is expired - put in a new Expiry date and send a new Reset code
                                        else:
                                            untilResetDate = set_reset_expiry(from_reset)
                                            # Create new ResetCode
                                            reset_key = create_resetpsw_key()
                                            # Write new Expiry and ResetCode into cardholder PDF
                                            text_resetcode_assign = json.dumps({"@ResetCode": reset_key,"@ResetExpiry": untilResetDate})
                                            json_resetcode_assign = json.loads(text_resetcode_assign)
                                            patch_mc_date = update_cardholder_pdf(CH_href, json_resetcode_assign)
                                            if patch_mc_date.status_code == 204:
                                                user_count+=1
                                                # TO DO: Send "Reset URL" to user
                                                print('----------------------------------------------') 
                                                print(" PASSWORD NOT CHANGED - Your RESET CODE was expired - A NEW RESET Code has been set and sent to "+data_CH_detail['@Email'])
                                                print('----------------------------------------------') 
                                                
                                                success_msg = "PASSWORD NOT CHANGED - Your RESET CODE was expired - A NEW RESET Code has been set and sent - Check your email and follow the Password Reset Link we sent you."
                                                #success_msg = data_CH_detail['@Email']
                                                success_code = 200
                                                return(success_msg, success_code) 
                                    else:    
                                        user_count=0
                                        error_notify = error_status("Reset Token is invalid or expired")
                                        print(error_notify)         
                                else:   
                                        user_count=0
                                        error_notify = error_status("No Reset Token")
                                        print(error_notify)  
                            else:
                                user_count=0
                                error_notify = error_status("Cardholder not valid")
                                print(error_notify)  
            else:
                user_count=0
                error_notify = error_status("Passwords didn't match")
                print(error_notify) 

        else:
            user_count=0
            error_notify = error_status("Email and/pr password is Empty")
            print(error_notify)
                    
        if (user_count == 0):  
            msg = "RESET PASSWORD FAILED - Unauthorized Reset Request"
            code = 400       
            return msg, code

        print('----- END RESET PASSWORD Script ---------------------------')
# ----------- End - FLASK ROUTES ------------------------------------ 

if __name__ == '__main__':
    app.run()



