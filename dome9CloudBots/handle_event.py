import re
import importlib
import logging
import os
from azure.identity import ClientSecretCredential

MININAL_TAG_LENGTH = 2
MININAL_ACTION_LENGTH = 1


def get_credentials():
    credentials = ClientSecretCredential(
        client_id=os.environ['AZURE_CLIENT_ID'],
        client_secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant_id=os.environ['AZURE_TENANT_ID']
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
        data['region'] = entity.get('region', '')
        data['region'] = data['region'].replace('_', '-')
    if 'remediationActions' in message:
        data['remediationActions'] = message['remediationActions']
    return data


def get_bots_from_finding(compliance_tags, remediation_actions):
    bots = []
    # Check if any of the tags have AUTO: in them. If there's nothing to do at all, skip it.
    auto_pattern = re.compile('AUTO:')
    for tag in compliance_tags:
        tag = tag.strip()  # Sometimes the tags come through with trailing or leading spaces.
        # Check the tag to see if we have AUTO: in it
        if auto_pattern.match(tag):
            tag_pattern = tuple(tag.split(' '))
            # The format is AUTO: bot_name param1 param2
            if len(tag_pattern) < MININAL_TAG_LENGTH:
                continue
            tag, bot, *params = tag_pattern
            bots.append([bot, params])

    for action in remediation_actions:
        action_pattern = tuple(action.split(' '))
        # The format is bot_name param1 param2
        if len(action_pattern) < MININAL_ACTION_LENGTH:
            continue
        bot, *params = action_pattern
        bots.append((bot, params))

    return bots


def handle_event(message, message_output):
    logging.info(f'{__file__} - handle event started')
    credentials = get_credentials()
    message_data = get_data_from_message(message)
    logging.info(f'{__file__} - message_data : {message_data}')
    if message_data.get('status') == 'Passed':
        logging.info(f'{__file__} - rule passed, no remediation needed')
        return False

    compliance_tags = message_data.get('compliance_tags')
    remediation_actions = message_data.get('remediationActions')
    bots = get_bots_from_finding(compliance_tags, remediation_actions)
    if not bots or not len(bots):
        print(f'''{__file__} - Rule: {message_data.get('rule_name')} Doesnt have any bots to run. Skipping.''')
        return False

    message_output['Rules violations found'] = []
    for bot_to_run in bots:
        bot_data = {}
        bot_data['Rule'] = message_data.get('rule_name')
        bot_data['ID'] = message_data.get('entity_id')
        bot_data['Name'] = message_data.get('entity_name')
        bot, params = bot_to_run
        bot_data['Remediation'] = bot
        logging.info(f'{__file__} - Bot name to execute: {bot}')
        try:
            bot_module = importlib.import_module(''.join(['bots.', bot]), package=None)
        except ImportError as e:
            bot_data['Bot'] = f'{bot} is not a known bot. skipping - {e}'
            continue

        try:  ## Run the bot
            bot_msg = bot_module.run_action(credentials, message['rule'], message['entity'], params)
            bot_data['Execution status'] = "passed"
        except Exception as e:
            bot_msg = f'Error while executing function {bot}. Error: {e}'
            bot_data['Execution status'] = "failed"
        bot_data['Bot message'] = bot_msg
        message_output['Rules violations found'].append(bot_data.copy())
    return True
