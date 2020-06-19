from azure.common.credentials import ServicePrincipalCredentials
import logging
import os
from azure.mgmt.resource import PolicyClient
import requests
import json
import adal

# Set Azure AD credentials from the environment variables
credentials = ServicePrincipalCredentials(
    client_id=os.environ['CLIENT_ID'],
    secret=os.environ['SECRET'],
    tenant=os.environ['TENANT']
)

def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    subscription_id = entity['accountNumber']
    pol_client = PolicyClient(credentials, subscription_id)
    azure_mgmt_url = "https://management.azure.com//subscriptions/" + subscription_id + "/providers/Microsoft.Authorization/policyAssignments/SecurityCenterBuiltIn?api-version=2019-09-01"
    authority_url = 'https://login.microsoftonline.com/'+ os.environ['TENANT']
    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(
        resource='https://management.azure.com/',
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['SECRET'],
    )
    token_path = 'Bearer ' + token["accessToken"]
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': token_path
    }
    pol_definition_id = entity['properties']['policyDefinitionId']
    
    payload = {"properties":{"policyDefinitionId":pol_definition_id, 
   
   "parameters":{ 
   
   "nextGenerationFirewallMonitoringEffect":{"value":"AuditIfNotExists"},
   
   }, 
   
    } 
   
   } 
    r = requests.put(azure_mgmt_url, json=payload, headers=headers)
    if r.status_code == 201:
        logging.info(f'Parameter set successfully')
    else:
        msg = r.status_code
        logging.info(f'Parameter not set ')
        logging.info(f'Error message contents {msg}')
