import re
import importlib
import logging
import os
from azure.common.credentials import ServicePrincipalCredentials

def get_credentials():
    credentials = ServicePrincipalCredentials(
        client_id = os.getenv('CLIEND_ID'),
        secret = os.getenv('SECRET'),
        tenant = os.getenv('TENANT')
    )
    return credentials

def get_data_from_message(message):
    data = {}
    if 'rule' in message:
        data['rule_name'] = message['rule'].get('name')
        if 'complianceTags' in message['rule']:
            # All of the remediation values are coming in on the compliance tags and they're pipe delimited
            data['compliance_tags'] = message['rule']['complianceTags'].split('|')
    if 'status' in message:
        data['status'] = message['status']
    entity = message.get('entity')
    if entity:
        data['entity_id'] = entity.get('id')
        data['entity_name'] = entity.get('name')
        data['region'] = entity.get('region')
    # Some events come through with 'null' as the region. If so, default to us-east-1
    if not data.get('region'):
        data['region'] = 'us-east-1'
    else:
        data['region'] = data['region'].replace('_', '-')
    return data


def handle_event(message, message_output):
    logging.info(f'{__file__} - handle event started')
    credentials= get_credentials()
    message_data = get_data_from_message(message)
    logging.info(f'{__file__} - message_data : {message_data}')
    if message_data.get('status') == 'Passed':
        logging.info(f'{__file__} - rule passed, no remediation needed')
        return False
    auto_pattern = re.compile('AUTO:')
    compliance_tags = message_data.get('compliance_tags')
    if not compliance_tags or not filter(auto_pattern.search, compliance_tags): #Rule Doesnt have any 'AUTO:' tags'
        return False    
    message_output['Rules violations found'] = []
    for tag in compliance_tags:
        logging.info(f'{__file__} - process tag : {tag}')
        tag = tag.strip()  # Sometimes the tags come through with trailing or leading spaces.
        # Check the tag to see if we have AUTO: in it
        pattern = re.compile('^AUTO:\s.+')
        bot_data = {}
        if pattern.match(tag):
            bot_data['Rule'] = message_data.get('rule_name')
            bot_data['ID'] = message_data.get('entity_id')
            bot_data['Name'] = message_data.get('entity_name')
            bot_data['Remediation'] = tag
            # Pull out only the bot verb to run as a function
            # The format is AUTO: bot_name param1 param2
            tag_pattern = tuple(tag.split(' '))
            if len(tag_pattern) < 2:
                bot_data['Empty Auto'] = 'tag. No bot was specified'
                continue    

            tag, bot, *params = tag_pattern
            try:
                bot_module = importlib.import_module(''.join(['bots.', bot]), package=None)
            except:
                bot_data['Bot'] = f'{bot} is not a known bot. skipping'
                continue

            try:  ## Run the bot
                bot_msg = bot_module.run_action(credentials ,message['rule'], message['entity'], params)
            except Exception as e:
                bot_msg = f'Error while executing function {bot}. Error: {e}'
            bot_data['Bot message'] = bot_msg     
            message_output['Rules violations found'].append(bot_data.copy())              
    return True