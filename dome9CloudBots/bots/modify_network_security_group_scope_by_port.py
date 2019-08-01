# What it does: Change network security group scope by a given port.
# Scope can be list of ip addresses with , between. example: 192.168.99.0/24,10.0.0.0/24,44.66.0.0/24
# Direction can be : source or destination
# Bot will remove Any from direction
# Usage: AUTO: modify_network_security_group_scope_by_port <port> <direction> <scope>
# Example: AUTO: modify_network_security_group_scope_by_port 556 source 10.0.0.0/24,172.16.0.1/32,168.243.22.0/23
# Limitations: None

from msrestazure.azure_exceptions import CloudError
from azure.mgmt.network import NetworkManagementClient
import logging


def modify_scope(rule, direction, scope):
    if len(scope) == 1:
        rule[f'{direction}_address_prefix'] = scope[0]
        rule[f'{direction}_address_prefixes'] = None
    else:
        rule[f'{direction}_address_prefixes'] = scope
        rule[f'{direction}_address_prefix'] = None


def is_port_in_range(port_to_find, ports_list):
    for port in ports_list:
        if port == port_to_find:
            return True
        else:
            port = port.split('-')
            if len(port) > 1 and port_to_find> port[0] and port_to_find< port[1]:
                return True
    return False


def run_action(credentials, rule, entity, params):
    port, direction, scope = params
    scope = scope.split(',')
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    resource_group_name = entity.get('resourceGroup', {}).get('name')
    nsg_name = entity.get('name')
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {resource_group_name} nsg_name : {nsg_name}')
    try:
        network_client = NetworkManagementClient(
            credentials,
            subscription_id
        )
        nsg = network_client.network_security_groups.get(resource_group_name, nsg_name)
        # Change nsg - NetworkSecurityGroup to dict
        nsg_dict = nsg.as_dict()
        security_rules = nsg_dict.get('security_rules')
        for rule in security_rules:
            if rule.get('destination_port_range'):
                if rule.get('destination_port_range') == port:
                    modify_scope(rule, direction, scope)
            elif rule.get('destination_port_ranges'):
                if is_port_in_range(port, rule.get('destination_port_ranges')):
                    modify_scope(rule, direction, scope)
        nsg_dict['security_rules'] = security_rules
        nsg_after_change = nsg.from_dict(nsg_dict)
        network_client.network_security_groups.create_or_update(resource_group_name, nsg_name, nsg_after_change)
        id = entity.get('id')
        msg = f'Network Security group name: {nsg_name} with id: {id} was modified, port: {port} direction:{direction} scope:{scope}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
    except CloudError as e:
        msg = f'unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
