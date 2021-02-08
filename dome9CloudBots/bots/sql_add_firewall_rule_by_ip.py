# What it does: Sets a firewall rule on Azure SQL Server ("whitelisted" IP addresses)
# Usage: sql_add_firewall_rule_by_ip - <firewall rule name> <firewall rule starting ip address> <firewall rule ending ip address>, supported values are IPv4 IP addresses
# Example: sql_add_firewall_rule_by_ip my_rule 10.0.0.0 10.254.254.254
# Limitations: CIDR blocks are not supported as rule values, must be individual starting and ending IP addresses
# Limitations: SQL Server "Deny public network access" value must be set to NO (default), or the bot will fail
# Last checked 20/1/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import Server


def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    firewall_rule_name, firewall_rule_start_ip, firewall_rule_end_ip = params
    if not firewall_rule_name:
        msg = 'Error! Firewall rule name is missing.'
        logging.info(f'{__file__} - {msg}')
    elif not firewall_rule_start_ip:
        msg = 'Error! Firewall rule starting IP is missing.'
        logging.info(f'{__file__} - {msg}')    
    elif not firewall_rule_end_ip:
        msg = 'Error! Firewall rule ending IP is missing.'
        logging.info(f'{__file__} - {msg}')

    logging.info(f'{__file__} - ${run_action.__name__} started')
    group_name = entity.get('resourceGroup', {}).get('name')
    subscription_id = entity.get('accountNumber')
    server_name = entity.get('name')
    server_location = entity.get('region')
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not subscription_id or not credentials:
        return raise_credentials_error()

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.firewall_rules.create_or_update(group_name, server_name, firewall_rule_name, firewall_rule_start_ip, firewall_rule_end_ip)        
        msg = f'Azure SQL firewall rule {firewall_rule_name} successfully on : {server_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    