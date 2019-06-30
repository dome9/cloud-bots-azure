import logging
import time
import azure.functions as func
import json
import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ))))
#Dot before file name use for relative path in Azure function app, need to be removed for local development
from .handle_event import *
from .send_events_and_errors import *
from .send_logs import *


def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Azure cloud bot function processed a request.')
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
      output_message['ReportTime'] = source_message.get('reportTime', 'N.A')
      output_message['Account id'] = source_message['account'].get('id', 'N.A')
      output_message['Finding key'] = source_message.get('findingKey', 'N.A')
      try:
        export_results = handle_event(source_message, output_message)
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
      if is_send_logs:    
        send_logs(output_message, start_time, source_message.get('account').get('vendor'))
  if output_message:
    return func.HttpResponse(f'{output_message}')
  else:
    return func.HttpResponse(f'Azure cloud bot had an error - {output_message}', status_code=400)
