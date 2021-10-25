# What it does: Sets a firewall rule on Azure SQL Server ("whitelisted" IP addresses)
# Usage: sql_add_firewall_rule_by_ip - <firewall rule name> <firewall rule starting ip address> <firewall rule ending ip address>, supported values are IPv4 IP addresses
# Example: sql_add_firewall_rule_by_ip my_rule 10.0.0.0 10.254.254.254
# Limitations: CIDR blocks are not supported as rule values, must be individual starting and ending IP addresses
# Limitations: SQL Server "Deny public network access" value must be set to NO (default), or the bot will fail
# Permissions: Microsoft.Sql/servers/firewallRules/write
# Last updated 9/2/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import Server, FirewallRule
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
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

    group_name = entity.get('resourceGroup', {}).get('name')
    subscription_id = entity.get('accountNumber')
    server_name = entity.get('name')
    server_location = entity.get('region')
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.firewall_rules.create_or_update(group_name, server_name, firewall_rule_name, parameters=FirewallRule(start_ip_address=firewall_rule_start_ip, end_ip_address=firewall_rule_end_ip))
        msg = f'Azure SQL firewall rule {firewall_rule_name} successfully on : {server_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed adding SQL firewall rule on {server_name}: {e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
