# What it does: Delete network security group 
# Deletion will be performed by given NSG
# Usage: delete_network_security_group
# Example: delete_network_security_group
# Limitations: None
# Permissions: Microsoft.Network/networkSecurityGroups/delete, Microsoft.Network/networkSecurityGroups/read
# Updated 8/2/21

from azure.core.exceptions import HttpResponseError
from azure.mgmt.network import NetworkManagementClient
import logging
import dome9CloudBots.bots_utils


def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    resource_group_name = entity.get('resourceGroup',{}).get('name')
    nsg_name = entity.get('name')
    logging.info(f'{__file__} - subscription_id : {subscription_id} - group_name : {resource_group_name} nsg_name : {nsg_name}')

    entity_type = entity.get('type')
    if not dome9CloudBots.bots_utils.is_correct_type(dome9CloudBots.bots_utils.EntitiesTypes.NETWORK_SECURITY_GROUP,
                                                     entity_type):
        error_msg = f'Error! entity type is not Network Security Group'
        logging.error(f'{__file__} - {error_msg}')
        raise TypeError(error_msg)

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    network_client = NetworkManagementClient(credentials, subscription_id)

    output_msg = ''

    try:                 
        network_client.network_security_groups.get(resource_group_name, nsg_name)     
        network_client.network_security_groups.begin_delete(resource_group_name, nsg_name)     
        id = entity.get('id')
        msg = f'Network Security group was deleted. id: {id}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:
        msg = f'Failed to delete network security group : {e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
