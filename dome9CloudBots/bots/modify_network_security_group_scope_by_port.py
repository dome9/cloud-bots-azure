# What it does: Change network security group rule scope by a given port.
# Scope can be list of ip addresses with , between. example: 192.168.99.0/24,10.0.0.0/24,44.66.0.0/24
# Direction can be : source or destination
# Access can be : Allow or Deny
# Bot will remove Any from direction
# In case you want to change port that equals to Any, you need to set port's value to *
# Usage: AUTO: modify_network_security_group_scope_by_port <port> <direction> <scope> <access>
# Example: AUTO: modify_network_security_group_scope_by_port 556 source 10.0.0.0/24,172.16.0.1/32,168.243.22.0/23 Allow
# Limitations: None
# Last updated 8/2/21

from azure.core.exceptions import HttpResponseError
from azure.mgmt.network import NetworkManagementClient
import logging
from itertools import chain

ONE_SCOPE = 1
ONE_PORT = 1
SEPARATOR = '-'


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

        if SEPARATOR in port:
            # Due to Azure SDK we split cases as port can be : '360' or '360-366'
            ports = port.split(SEPARATOR)
            starting_port, ending_port = ports
            if is_port_range(ports) and starting_port <= port_to_find <= ending_port:
                return True
    return False


def run_action(credentials, rule, entity, params):
    port, direction, scope, access, *_ = chain(params, [None])
    scope = scope.split(',')
    logging.info(f'{__file__} - run_action started')

    subscription_id = entity.get('accountNumber')
    entity_type = entity.get('type')
    
    if entity_type == 'VirtualMachine':
        logging.info(f'Entity is a VM')
        # nsg_name = entity['nics'][0]['networkSecurityGroup']['name']
        # resource_group_name = entity['nics'][0]['networkSecurityGroup']['resourceGroup']['name']

        num_of_nics = len(entity['nics'])
        nsg_names = [entity['nics'][i]['networkSecurityGroup']['name'] for i in range(num_of_nics)]  # get names of nics
        resource_group_names = [entity['nics'][i]['networkSecurityGroup']['resourceGroup']['name']
                                for i in range(num_of_nics)]  # get names of the nic resource group

        nsgs_and_resource_groups = zip(nsg_names, resource_group_names)

    else:
        logging.info(f'Entity is an NSG')
        resource_group_names = [entity.get('resourceGroup', {}).get('name')]
        nsg_names = [entity.get('name')]

        nsgs_and_resource_groups = zip(nsg_names, resource_group_names)

    output_msg = ''

    for nsg_name, resource_group_name in nsgs_and_resource_groups:
        logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {resource_group_name} nsg_name : {nsg_name}')

        try:
            network_client = NetworkManagementClient(
                credentials,
                subscription_id
            )
            nsg = network_client.network_security_groups.get(resource_group_name, nsg_name)

            # Change nsg - NetworkSecurityGroup to dict
            modified = False
            nsg_dict = nsg.as_dict()
            security_rules = nsg_dict.get('security_rules')
            for rule in security_rules:

                if rule.get('destination_port_range'):
                    if rule.get('destination_port_range') == port:
                        modify_scope(rule, direction, scope, access)
                        modified = True

                elif rule.get('destination_port_ranges'):
                    if is_port_in_range(port, rule.get('destination_port_ranges')):
                        modify_scope(rule, direction, scope, access)
                        modified = True

            if not modified:
                continue

            nsg_dict['security_rules'] = security_rules
            nsg_after_change = nsg.from_dict(nsg_dict)
            network_client.network_security_groups.begin_create_or_update(resource_group_name,
                                                                          nsg_name, nsg_after_change)
            entity_id = entity.get('id')
            log_msg = f'Network Security group name: {nsg_name} with id: {entity_id} was modified, port: {port} ' \
                      f'direction:{direction} scope:{scope}\n'
            logging.info(f'{__file__} - {log_msg}')
            output_msg += log_msg

        except HttpResponseError as e:
            log_msg = f'Request to Azure failed on network security group: {nsg_name} -\n {e.message}'
            logging.info(f'{__file__} - {log_msg}')
            output_msg += log_msg

        except Exception as e:
            log_msg = f'Unexpected exception: {e}'
            logging.info(f'{__file__} - {log_msg}')
            output_msg += log_msg
            return output_msg

    return output_msg


