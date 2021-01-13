# What it does: Allows Storage account access to all subnets in all VNets in a subscription
# Usage: storage_account_enable_access_from_all_vnets
# Limitations: None
# Last checked 13/1/21

import logging
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountUpdateParameters, NetworkRuleSet, VirtualNetworkRule)
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import ServiceEndpointPropertiesFormat, Subnet, ServiceEndpointPropertiesFormat
from azure.core.exceptions import HttpResponseError, ResourceExistsError
def raise_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg

def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    subscription_id = entity['accountNumber']
    group_name = entity['resourceGroup']['name']
    storage_account_name = entity['name']
    storage_account_region = entity['region']
    
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - storage_account : {storage_account_name}')
    
    if not subscription_id or not credentials:
        return raise_credentials_error()

    try:  
        network_client = NetworkManagementClient(credentials,subscription_id)
        storage_client = StorageManagementClient(credentials, subscription_id)

        vnets = network_client.virtual_networks.list_all()
        acls = []
        endpoint_params = [ServiceEndpointPropertiesFormat(service='Microsoft.Storage', locations=["*"])]

        for v in vnets:
            vnet_name = v.name
            vnet_nsg_split = v.id.split('/')
            vnet_nsg = vnet_nsg_split[4]
            subnets = v.subnets
            vnet_region = v.location
            if storage_account_region == vnet_region:
                logging.info(f'Regions match - applying ACLs to {vnet_name}')
                for s in subnets:
                    subnet_path = s.id
                    subnet_name = s.name
                    subnet_address_prefix = s.address_prefix
                    service_endpoint_list = s.service_endpoints
                    logging.info(f'Subnet path :  {subnet_path} Subnet Name : {subnet_name} Subnet CIDR : {subnet_address_prefix} Endpoint list : {service_endpoint_list}')
            
                    # Create storage endpointif doesn't exist
                    network_client.subnets.begin_create_or_update(resource_group_name=vnet_nsg, virtual_network_name=vnet_name, subnet_name=subnet_name,
                        subnet_parameters=Subnet(address_prefix=subnet_address_prefix, service_endpoints=endpoint_params))
                    
                    acls.append(VirtualNetworkRule(virtual_network_resource_id=subnet_path))            
                storage_client.storage_accounts.update(group_name,storage_account_name, StorageAccountUpdateParameters(network_rule_set=NetworkRuleSet(default_action='Deny', virtual_network_rules=acls)))
            else:
               logging.info(f'Regions do not match - skipping {vnet_name}')

        
    except (CloudError, HttpResponseError, ResourceExistsError) as e:
        logging.info(f'An error occured : {e}')   
