# What it does: Change network security group scope by a given port.
# Scope can be list of ip addresses with , between. example: 192.168.99.0/24,10.0.0.0/24,44.66.0.0/24
# Direction can be : source or destination
# Bot will remove Any from direction
# Access can be : Allow or Deny
# Usage: AUTO: modify_network_security_group_scope_by_port <port> <direction> <scope> <access>
# Example: AUTO: modify_network_security_group_scope_by_port 556 source 10.0.0.0/24,172.16.0.1/32,168.243.22.0/23 Allow
# Limitations: None

from msrestazure.azure_exceptions import CloudError
from azure.mgmt.network import NetworkManagementClient
import logging
from itertools import chain

ONE_SCOPE = 1
ONE_PORT = 1


def is_port_range(port):
    return len(port) > ONE_PORT


def modify_scope(rule, direction, scope, access):
    scope_ips_length = len(scope)
    if scope_ips_length == ONE_SCOPE:
        rule[f'{direction}_address_prefix'] = scope[0]
        rule[f'{direction}_address_prefixes'] = None
    else:
        rule[f'{direction}_address_prefixes'] = scope
        rule[f'{direction}_address_prefix'] = None
    rule['access'] = access or rule['access']


def is_port_in_range(port_to_find, ports_list):
    for port in ports_list:
        if port == port_to_find:
            return True

        else:
            # Due to Azure SDK we split cases as port can be : '360' or '360-366'
            ports = port.split('-')
            starting_port, ending_port = ports
            if is_port_range(ports) and port_to_find > starting_port and port_to_find < ending_port:
                return True

    return False


def run_action(credentials, rule, entity, params):
    port, direction, scope, access, *_ = chain(params, [None])
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
                    modify_scope(rule, direction, scope, access)

            elif rule.get('destination_port_ranges'):
                if is_port_in_range(port, rule.get('destination_port_ranges')):
                    modify_scope(rule, direction, scope, access)

        nsg_dict['security_rules'] = security_rules
        nsg_after_change = nsg.from_dict(nsg_dict)
        network_client.network_security_groups.create_or_update(resource_group_name, nsg_name, nsg_after_change)
        entity_ID = entity.get('id')
        msg = f'Network Security group name: {nsg_name} with id: {entity_ID} was modified, port: {port} direction:{direction} scope:{scope}'
        logging.info(f'{__file__} - {msg}')

        return f'{msg}'

    except CloudError as e:
        msg = f'unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')

        return f'{msg}'
