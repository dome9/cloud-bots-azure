# What it does: Delete network security group rule
# Deletion will be preformed by given destination port, destination scope, source port, source scope and access
# Access can be : Allow or Deny
# Usage: AUTO: delete_network_security_group_single_rule <destination port> <destination scope> <source port> <source scope> <access>
# Example: AUTO: delete_network_security_group_single_rule 556 10.0.0.0/24 22 0.0.0.0/2 Allow
# In case you don't want to use specific destination you need to fill '-' in the specific field.
# Example 1: AUTO: delete_network_security_group_single_rule 556 10.0.0.0/24 - - Allow
# Example 2: AUTO: delete_network_security_group_single_rule - - 22 0.0.0.0/2 Deny
# Limitations: None
# Updated 8/2/21

from azure.core.exceptions import HttpResponseError
from azure.mgmt.network import NetworkManagementClient
import logging

ONE_PORT = 1
SEPARATOR = '-'

def is_port_range(port):
    return len(port) > ONE_PORT


def is_port_in_range(port_to_find, ports_list):
    for port in ports_list:
        if port == port_to_find:
            return True

        if SEPARATOR in port:
            # Due to Azure SDK we split cases as port can be : '360' or '360-366'
            ports = port.split(SEPARATOR)
            starting_port, ending_port = ports
            if is_port_range(ports) and starting_port <= port_to_find <= ending_port:
                return True
    return False

def is_port_match(rule, direction, port):
    port_to_find = rule.get(f'{direction}_port_range')
    ports_to_find = rule.get(f'{direction}_port_ranges')
    if port_to_find:
        if port_to_find == port:
            return True

        else:
            ports = port_to_find.split('-')
            if len(ports) > ONE_PORT:
                starting_port, ending_port = ports
                if is_port_range(ports) and starting_port <= port <= ending_port:
                    return True

    elif ports_to_find:
        if is_port_in_range(port, ports_to_find):
            return True

    return False

def is_scope_match(rule, direction, scope):
    return rule[f'{direction}_address_prefix'] == scope or scope == SEPARATOR

def is_access_match(rule, access):
    return rule['access'] == access.capitalize() # this must be Allow or Deny

def is_rule_should_be_deleted_by_direction(rule, direction, port, scope, access):
    return is_port_match(rule, direction, port) and is_scope_match(rule, direction, scope) and is_access_match(rule,
                                                                                                               access)

def is_rule_should_be_deleted(rule, destination_port, destination_scope, source_port, source_scope, access):
    destination = [destination_port, destination_scope]
    source = [source_port, source_scope]
    ## Case need to check both destination and source
    if all(item != SEPARATOR for item in destination + source):
        return is_rule_should_be_deleted_by_direction(rule, 'destination', destination_port, destination_scope,
                                                      access) and is_rule_should_be_deleted_by_direction(rule, 'source',
                                                                                                         source_port,
                                                                                                         source_scope,
                                                                                                         access)
    ## Case need to check only destination
    if destination[0] != SEPARATOR and all(item == SEPARATOR for item in source):
        return is_rule_should_be_deleted_by_direction(rule, 'destination', destination_port, destination_scope, access)

    ## Case need to check only source
    if source[0] != SEPARATOR and all(item != SEPARATOR for item in source):
        return is_rule_should_be_deleted_by_direction(rule, 'source', source_port, source_scope, access)

    return False

def run_action(credentials, rule, entity, params):
    destination_port, destination_scope, source_port, source_scope, access = params
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

        nsg_dict = nsg.as_dict()
        security_rules = nsg_dict.get('security_rules')
        for rule in security_rules:
            if is_rule_should_be_deleted(rule, destination_port, destination_scope, source_port, source_scope, access):
                security_rules.remove(rule)

        nsg_dict['security_rules'] = security_rules
        nsg_after_change = nsg.from_dict(nsg_dict)
        network_client.network_security_groups.begin_create_or_update(resource_group_name, nsg_name, nsg_after_change)
        entity_ID = entity.get('id')
        msg = f'Network Security group name: {nsg_name} with id: {entity_ID} was modified'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')

        return f'{msg}'
