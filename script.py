import os, sys, time
from ringcentral import SDK

RECIPIENT    = "+19544043185"
TEXT_MESSAGE = "..."
SERVER_URL = "https://platform.devtest.ringcentral.com"
CLIENT_ID = "83kBdTbHuj3b725OPcJAh8"
CLIENT_SECRET = "VdaUotnMJpgbyVfcM8w7MV5K5LMdJmULud0QlzWigqKj"
JWT_TOKEN = "eyJraWQiOiI4NzYyZjU5OGQwNTk0NGRiODZiZjVjYTk3ODA0NzYwOCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJhdWQiOiJodHRwczovL3BsYXRmb3JtLmRldnRlc3QucmluZ2NlbnRyYWwuY29tL3Jlc3RhcGkvb2F1dGgvdG9rZW4iLCJzdWIiOiI4MzIwMDUwMDUiLCJpc3MiOiJodHRwczovL3BsYXRmb3JtLmRldnRlc3QucmluZ2NlbnRyYWwuY29tIiwiZXhwIjozODQzOTQ2NDkxLCJpYXQiOjE2OTY0NjI4NDQsImp0aSI6IkxGOE1uZWVqU3gyNTVzQmtGMGtseUEifQ.E0bsjqODsBoPdUCBoivUOlrRhCm2-B3ug3AH0L8OFx1uFg47PeX4yn3QUud1rb_yIL7NqbAf5oYiYNyEZAX2rHtwvhxaitBRCA_aq-PstT7C4E7bhvC14Buxk6OLmDqRi2qj3PBkn_gRzo2RedmwxP65yyGsqE1yHfVrvjltSkKxCV5-2iANJRHhGY5H4-MtBEt73qwo6YL5oFSBCm_rAZN1VOtA2yAEVmuRhtIWbK5u0LZcbX9LafAapIzkWDnnj4cwFW5_6Wu2O0Yn6GKvnPyvL-us1VCNKZkTsWYbpl224frALW7HUakYAJFX5UqYbeeDjeVvY40RMDWnSNb2DA"

# Read phone number(s) that belongs to the authenticated user and detect if a phone number
# has the SMS capability
def read_extension_phone_number_detect_sms_feature():
    try:
        resp = platform.get("/restapi/v1.0/account/~/extension/~/phone-number")
        jsonObj = resp.json()
        for record in jsonObj.records:
            for feature in record.features:
                if feature == "SmsSender":
                    # If user has multiple phone numbers, check and decide which number
                    # to be used for sending SMS message.
                    return send_sms(record.phoneNumber)
        if len(jsonObj.records) == 0:
            print("This user does not own a phone number!")
        else:
            print("None of this user's phone number(s) has the SMS capability!")
    except Exception as e:
        print(e)

# Send a text message from a user own phone number to a recipient number
def send_sms(fromNumber):
    try:
        bodyParams = {
            'from' : { 'phoneNumber': fromNumber },
            'to'   : [ {'phoneNumber': RECIPIENT } ],
            'text' : TEXT_MESSAGE
        }
        endpoint = "/restapi/v1.0/account/~/extension/~/sms"
        resp = platform.post(endpoint, bodyParams)
        jsonObj = resp.json()
        print("SMS sent. Message id: " + str(jsonObj.id))
        check_message_status(jsonObj.id)
    except Exception as e:
        print(e)

# Check the sending message status until it's out of the queued status
def check_message_status(messageId):
    try:
        endpoint = "/restapi/v1.0/account/~/extension/~/message-store/" + str(messageId)
        resp = platform.get(endpoint)
        jsonObj = resp.json()
        print("Message status: " + jsonObj.messageStatus)
        if jsonObj.messageStatus == "Queued":
            time.sleep(2)
            check_message_status(jsonObj.id)
    except Exception as e:
        print(e)

# Instantiate the SDK and get the platform instance
rcsdk = SDK(CLIENT_ID, CLIENT_SECRET, SERVER_URL)
platform = rcsdk.platform()

# Authenticate a user using a personal JWT token
def login():
    try:
        platform.login(jwt= JWT_TOKEN )
        read_extension_phone_number_detect_sms_feature()
    except Exception as e:
        sys.exit("Unable to authenticate to platform. Check credentials." + str(e))

login()
