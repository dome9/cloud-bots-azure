# What it does: Enables flow logs on an Azure Network Security Group. 
# Usage: enable_nsg_flow_logs <storage-account-name> <storage-account-resource-group> <network-watcher-name> <log-retention-days> <flow-log-name>
# Example: enable_nsg_flow_logs my-storage-account storage-resource-group NetworkWatcher_northeurope 30 myflowlog
# Limitations: None
# Permissions: Microsoft.Network/networkWatchers/flowLogs/write, Microsoft.Storage/storageAccounts/listKeys/action
# Last checked 8/2/21

from azure.core.exceptions import HttpResponseError
from azure.mgmt.network import NetworkManagementClient
import logging
import dome9CloudBots.bots_utils

nw_resource_group_name = 'NetworkWatcherRG'


def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    storage_account_name, sa_resource_group_name, network_watcher_name, retention_days, flow_log_name = params
    subscription_id = entity.get('accountNumber')
    region = entity.get('region')
    nsg_name = entity.get('name')
    
    logging.info(f'{__file__} - subscription_id : {subscription_id} - nsg_name : {nsg_name}')
    
    target_resource_path = entity.get('id')
    storage_account_path = '/subscriptions/' + subscription_id + '/resourceGroups/' + sa_resource_group_name + \
                           '/providers/Microsoft.Storage/storageAccounts/' + storage_account_name

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

    flow_log_parameters = {
        'location':region,
        'target_resource_id': target_resource_path,
        'storage_id': storage_account_path,
        'enabled':True,
        'retention_policy': {'days': retention_days, 'enabled': True},
        'format': {'type': 'JSON', 'version': 2}
    }

    output_msg = ''

    try:
        network_client.flow_logs.begin_create_or_update(nw_resource_group_name, network_watcher_name, flow_log_name, flow_log_parameters)
        msg = f'Network Security group flow logs have been enabled on: {nsg_name}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except HttpResponseError as e:   
        msg = f'Failed enabling flow logs on {nsg_name} : {e.message}'
        logging.info(f'{__file__} - {msg}') 
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
