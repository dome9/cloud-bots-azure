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
        print(' in loop after credentials ')
        inbound_rules = entity.get('inboundRules')        
        for r in (inbound_rules):
            if ((r['source']) == '0.0.0.0/0') and ((r['destination']) == '0.0.0.0/0') and ((r['destinationPort']) == 22) or ((r['destinationPortTo']) == 22)  \
                and ((r['direction']) == 'INBOUND') and ((r['action']) == 'ALLOW'):
                    sgrule = (r['name'])
                    print('Security Group rule name to be deleted is: ' + sgrule)
                    network_client.security_rules.delete(resource_group_name, nsg_name, sgrule)
                    msg = f'Network Security group name: {nsg_name} rule name {sgrule} was deleted successfully'
                    logging.info(f'{__file__} - {msg}')
            else:
                    msg = f'ERROR: Network Security group name: {nsg_name} was not updated successfully'
                    logging.info(f'{__file__} - {msg}')
    except CloudError as e:
        msg = f'unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')

        return f'{msg}'
    