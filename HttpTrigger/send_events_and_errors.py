import logging
import os
import json
from sendgrid import SendGridAPIClient



def sendEvent(output_message):
    logging.info(f'{__file__} - send event')
    message = {
    'personalizations': [
        {
            'to': [
                {
                    'email': os.getenv('OUTPUT_EMAIL')
                }
            ],
            'subject': 'Azure Remediation Output'
        }
    ],
    'from': {
        'email': 'azure@cloudBots.com'
    },
    'content': [
        {
            'type': 'text/plain',
            'value': json.dumps(output_message)
        }
    ]
    }

    try:
        sg = SendGridAPIClient(os.getenv('SEND_GRID_API_CLIENT'))
        response = sg.send(message)
        logging.info(f'{__file__} - send event respone status : {response.status_code}')

    except Exception as e:
        logging.info(f'{__file__} - send event failed, error: : {e}')
