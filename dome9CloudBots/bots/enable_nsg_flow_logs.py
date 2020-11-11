# What it does: Enables flow logs on an Azure Network Security Group. 
# Usage: enable_nsg_flow_logs <storage-account-name> <storage-account-resource-group> <network-watcher-name> <log-retention-days> <flow-log-name>
# Example: enable_nsg_flow_logs my-storage-account storage-resource-group NetworkWatcher_northeurope 30 myflowlog
# Limitations: None

from msrestazure.azure_exceptions import CloudError
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network.models import NetworkSecurityGroup, SecurityRule, FlowLog
import logging

nw_resource_group_name = 'NetworkWatcherRG'

def run_action(credentials ,rule, entity, params):
    storage_account_name, sa_resource_group_name, network_watcher_name, retention_days, flow_log_name = params
    logging.info(f'{__file__} - run_action started')
    subscription_id = entity.get('accountNumber')
    region = entity.get('region')
    nsg_name = entity.get('name')
    
    logging.info(f'{__file__} - subscription_id : {subscription_id} - nsg_name : {nsg_name}')
    
    target_resource_path = entity.get('id')
    storage_account_path = '/subscriptions/' + subscription_id + '/resourceGroups/' + sa_resource_group_name + '/providers/Microsoft.Storage/storageAccounts/' + storage_account_name
    if not subscription_id or not credentials:
        msg = 'Error! Subscription id or Resource group name are missing.'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}' 
    
    network_client = NetworkManagementClient(credentials, subscription_id)

    flow_log_parameters = {
        'location':region,
        'target_resource_id': target_resource_path,
        'storage_id': storage_account_path,
        'enabled':True,
        'retention_policy':{'days':retention_days, 'enabled':True},
        'format':{'type':'JSON', 'version':2}
    }

    try:
        network_client.flow_logs.begin_create_or_update(nw_resource_group_name, network_watcher_name, flow_log_name, flow_log_parameters)
        msg = f'Network Security group flow logs have been enabled on: {nsg_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'
    except CloudError as e:   
        msg = f'unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}') 
        return f'{msg}'