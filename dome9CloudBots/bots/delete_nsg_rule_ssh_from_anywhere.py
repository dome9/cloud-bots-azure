# What it does: Delete any network security group rules that allows SSH access from anywhere (0.0.0.0/0)
# Usage: AUTO: delete_ssh_rule_rdp_from_anywhere
# Limitations: None

from msrestazure.azure_exceptions import CloudError
from azure.mgmt.network import NetworkManagementClient
import logging

def run_action(credentials, rule, entity, params):
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
        inbound_rules = entity.get('inboundRules')        
        for r in (inbound_rules):
            if ('0.0.0.0/0' in r['source'] and '0.0.0.0/0' in r['destination'] and r['destinationPort'] == 22 and r['destinationPortTo'] == 22 \
                and 'INBOUND' in r['direction'] and 'ALLOW' in r['action']):
                    sg_rule = (r['name'])
                    print('Security Group rule name to be deleted is: ' + sg_rule)
                    network_client.security_rules.delete(resource_group_name, nsg_name, sg_rule)
                    msg = f'Network Security group name: {nsg_name} rule name {sg_rule} was deleted successfully'
                    logging.info(f'{__file__} - {msg}')
            else:
                    sg_rule = (r['name'])
                    msg = f'Network Security group rule: {sg_rule} does not meet the deletion criteria'
                    logging.info(f'{__file__} - {msg}')
    except CloudError as e:
        msg = f'unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')

        return f'{msg}'
    