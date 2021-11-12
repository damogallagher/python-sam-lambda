import json
from shared_opsgenie import get_alert_api
from common_code import  error_response, success_response
import opsgenie_sdk
from opsgenie_sdk.rest import ApiException

alert_api = get_alert_api()

# Create an OpsGenie Alert
# See https://docs.opsgenie.com/docs/python-sdk-alert#create-alert and
# https://docs.opsgenie.com/docs/opsgenie-python-sdk-configurations and
# https://docs.opsgenie.com/docs/alert-api#section-create-alert
def lambda_handler(event, context):

    if not event or not event["body"]:
        return error_response("Request body is not specified. Please pass in the OpsGenie details in the request body")     

    print("event:", event)
    body = event["body"]
    print("body:", body)
    request_body = json.loads(event["body"])
    print("request_body:", request_body)

    create_alert_payload_dict = populate_create_alert_payload(request_body)

    error_messages = validate_create_alert_payload(create_alert_payload_dict)
    if len(error_messages) > 0:
        return error_response(json.dumps(error_messages, default=str))

    body = opsgenie_sdk.CreateAlertPayload(**create_alert_payload_dict)
    try:
        create_response = alert_api.create_alert(create_alert_payload=body)
        print("create_response:", create_response)
        return success_response(json.dumps(create_response, default=str))
    except ApiException as err:
        print("Exception when calling AlertApi->create_alert: %s\n" % err)



def get_body_value(create_alert_payload_dict, request_body, key, default_value):
    if key in request_body:
        value = request_body[key]
        create_alert_payload_dict[key] = value

def populate_create_alert_payload(request_body):
    create_alert_payload_dict = {}
    get_body_value(create_alert_payload_dict, request_body,'message', '')
    get_body_value(create_alert_payload_dict, request_body,'alias', '')
    get_body_value(create_alert_payload_dict, request_body,'description', '')
    get_body_value(create_alert_payload_dict, request_body,'responders', [])
    get_body_value(create_alert_payload_dict, request_body,'visible_to', [])
    get_body_value(create_alert_payload_dict, request_body,'actions', [])
    get_body_value(create_alert_payload_dict, request_body,'tags', [])
    get_body_value(create_alert_payload_dict, request_body,'details', {})
    get_body_value(create_alert_payload_dict, request_body,'entity', '')
    get_body_value(create_alert_payload_dict, request_body,'source', '')
    get_body_value(create_alert_payload_dict, request_body,'priority', '')
    get_body_value(create_alert_payload_dict, request_body,'user', '')
    get_body_value(create_alert_payload_dict, request_body,'note', '')

    return create_alert_payload_dict

def validate_create_alert_payload(create_alert_payload_dict):
    error_messages = []

    if 'message' not in create_alert_payload_dict:
        error_messages.append("Please specify a message - this is the only required parameter")  
    elif len(create_alert_payload_dict['message']) > 130:
        error_messages.append("message can only be 130 charachters long")    

    if 'alias' in create_alert_payload_dict and len(create_alert_payload_dict['alias']) > 512:
        error_messages.append("alias can only be 512 charachters long") 

    if 'description' in create_alert_payload_dict and len(create_alert_payload_dict['description']) > 15000:
        error_messages.append("description can only be 15000 charachters long") 

    if 'responders' in create_alert_payload_dict and len(create_alert_payload_dict['responders']) > 50:
        error_messages.append("you can only specify 50 responders") 

    if 'visible_to' in create_alert_payload_dict and len(create_alert_payload_dict['visible_to']) > 50:
        error_messages.append("you can only specify 50 groups this alert is visibleTo") 

    if 'actions' in create_alert_payload_dict:
        if len(create_alert_payload_dict['actions']) > 10:
            error_messages.append("you can only specify 10 actions") 
        for action in create_alert_payload_dict['actions']:
            if len(action) > 50:
                error_messages.append("The action '" + action + " needs to be less than 50 charachters") 
    
    if 'tags' in create_alert_payload_dict:
        if len(create_alert_payload_dict['tags']) > 20:
            error_messages.append("you can only specify 20 tags") 
        for tag in create_alert_payload_dict['tags']:
            if len(tag) > 50:
                error_messages.append("The tag '" + tag + " needs to be less than 50 charachters") 

    if 'details' in create_alert_payload_dict and len(create_alert_payload_dict['details']) > 8000:
        error_messages.append("details can only be 8000 charachters long") 

    if 'entity' in create_alert_payload_dict and len(create_alert_payload_dict['entity']) > 512:
        error_messages.append("entity can only be 512 charachters long") 

    if 'source' in create_alert_payload_dict and len(create_alert_payload_dict['source']) > 100:
        error_messages.append("source can only be 100 charachters long") 

    if 'priority' in create_alert_payload_dict and create_alert_payload_dict['priority'] not in ['P1', 'P2', 'P3', 'P4', 'P5']:
        error_messages.append("Please specify a priority of P1, P2, P3, P4 or P5")   

    if 'user' in create_alert_payload_dict and len(create_alert_payload_dict['user']) > 100:
        error_messages.append("user can only be 100 charachters long") 

    if 'note' in create_alert_payload_dict and len(create_alert_payload_dict['note']) > 25000:
        error_messages.append("note can only be 25000 charachters long")         
    return error_messages    
