import logging
import time
import azure.functions as func
import json
import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
#Dot before file name use for relative path in Azure function app, need to be removed for local development
import hashlib
import base64
import hmac
from .handle_event import *
from .send_events_and_errors import *
from .send_logs import *


def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Azure cloud bot function processed a request.')
    #Basic Auth Support
  if os.getenv('BASIC_AUTH_ENABLED') and os.getenv(
      'BASIC_AUTH_ENABLED') == "1":
    basic_auth_username = os.getenv('BASIC_AUTH_USERNAME')
    basic_auth_password = os.getenv('BASIC_AUTH_PASSWORD')
    # Make creds to bytes
    if "authorization" not in dict(req.headers).keys():
      logging.info(
        "Request missing authorization header. Returning 401 Unauthorized."
      )
      return func.HttpResponse(f'Unauthorized', status_code=401)

    # Make creds to bytes
    string_requester_credentials = str.split(
      req.headers['Authorization'])[1]
    logging.debug(string_requester_credentials)
    byte_requester_credentials = base64.b64decode(
      string_requester_credentials.encode('ascii'), validate=True)
    byte_stored_credentials = (basic_auth_username + ":" +
                   basic_auth_password).encode('ascii')

    #Make bytes to hashes
    stored_credentials = hashlib.sha256()
    stored_credentials.update(byte_stored_credentials)
    stored_credentials = stored_credentials.digest()

    requester_credentials = hashlib.sha256()
    requester_credentials.update(byte_requester_credentials)
    requester_credentials = requester_credentials.digest()

    #Compare hashes
    if hmac.compare_digest(requester_credentials, stored_credentials):
      logging.info("Request is authorized.")
    else:
      return func.HttpResponse(f'Unauthorized', status_code=401)

  try:
    source_message = req.get_json()
  except Exception as e:
    logging.info('Bad request.')
    return func.HttpResponse(f'Azure cloud bot had an error', status_code=400)
    
  start_time = time.time()
  logging.info(f'{__file__} - source message : {source_message}')
  output_message = {}
  if source_message:
      logging.info(f'source message : {source_message}')
      output_message['Account id'] = source_message['account'].get('id', 'N.A')
      output_message['Finding key'] = source_message.get('findingKey', 'N.A')
      try:
        export_results = handle_event(source_message, output_message)
        send_logs_api_gateway(output_message)  # todo - check with omer if it is the wanted behavior
      except Exception as e:
        export_results = True
        logging.info(f'{__file__} - Handle event failed')
        output_message['Handle event failed'] = str(e)
      if export_results:
        if os.getenv('OUTPUT_EMAIL'):
          sendEvent(output_message)
      else:
        logging.info(f'''{__file__} - Output didn't sent : {output_message}''')
      is_send_logs = os.getenv('SEND_LOGS', False)  
      logging.info(f'{__file__} - SEND_LOGS set to {str(is_send_logs)}')  
      if is_send_logs: # todo - ask omer about it. we send logs to sumo. what is the behavior we want?
        send_logs(output_message, start_time, source_message.get('account').get('vendor'))
  if output_message:
    return func.HttpResponse(f'{output_message}')
  else:
    return func.HttpResponse(f'Azure cloud bot had an error - {output_message}', status_code=400)
