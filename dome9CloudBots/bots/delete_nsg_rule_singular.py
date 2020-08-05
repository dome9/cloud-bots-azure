# What it does: Delete network security group rule
# Deletion will be preformed by given destination port, destination scope, source port, source scope and access
# Access can be : Allow or Deny
# Usage: AUTO: delete_nsg_rule_singular <destination port> <destination scope> <source port> <source scope> <access>
# Example: AUTO: delete_nsg_rule_singular 556 10.0.0.0/24 22 0.0.0.0/2 Allow
# In case you don't want to use specific destination you need to fill '-' in the specific field.
# Example 1: AUTO: delete_nsg_rule_singular 556 10.0.0.0/24 - - Allow
# Example 2: AUTO: delete_nsg_rule_singular - - 22 0.0.0.0/2 Deny
# Limitations: Comma seperated values not supported in this release

from msrestazure.azure_exceptions import CloudError
from azure.mgmt.network import NetworkManagementClient
import logging
import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network.v2019_02_01.models import SecurityRule, SecurityRulePaged

def run_action(credentials, rule, entity, params):
    destination_port, destination_scope, source_port, source_scope, access = params
      
    subscription_id = entity.get('accountNumber')
    resource_group_name = entity.get('resourceGroup', {}).get('name')
    nsg_name = entity.get('name')
    logging.error(f'{__file__} - subscription_id : {subscription_id} - group_name : {resource_group_name} nsg_name : {nsg_name}')

    try:
        # Instantiate Network Client Connection
        network_client = NetworkManagementClient(
            credentials,
            subscription_id
                )

        # Set field to be ignored on AUTO tag
        ignore_field = '-'

        # Set fields to check
        src_port_field_check = True
        src_address_scope_field_check = True
        dest_port_field_check = True
        dest_address_scope_field_check = True
        action_field_check = True
        is_source_port_range = False
        is_dest_port_range = False
        fields_to_match = 5

        if source_port == ignore_field:
            src_port_field_check = False
            fields_to_match = fields_to_match - 1
        if source_scope == ignore_field:
            src_address_scope_field_check = False
            fields_to_match = fields_to_match - 1
        if destination_port == ignore_field:
            dest_port_field_check = False
            fields_to_match = fields_to_match - 1
        if destination_scope == ignore_field:
            dest_address_scope_field_check = False
            fields_to_match = fields_to_match - 1
        if access == ignore_field:
            action_field_check = False
            fields_to_match = fields_to_match - 1
            
        # logging.error(f'Number of fields to match is ', fields_to_match, '\n')

        logging.info(f'Source port field check set to {src_port_field_check}')
        logging.info(f'Source address scope field check set to {src_address_scope_field_check}')
        logging.info(f'Destination port field check set to {dest_port_field_check}')
        logging.info(f'Destination address scope field check set to {dest_address_scope_field_check}')
        logging.info(f'Action field check set to {action_field_check}')

        # List each rule in the RG and NSG name passed from the payload       
        nsg = network_client.security_rules.list(resource_group_name, nsg_name)
        for r in nsg:
            # Get rule name using split function
            rule_id = r.id.split('/')
            rule_name = rule_id[10]
            # Set a counter to determine how many fields we have to match before we delete an NSG rule, starting with match all
            # If we find a - in a field, we ignore it and decrement the number of matches we need to have to run the delete
            #fields_to_match = 5
            # Reset match counter, we will only delete the rule when both fields_to_match and match_counter are equal
            match_counter = 0
            
            logging.info(f'Reading NSG rule...')
            logging.info(f'RULE NAME         | {rule_name}')
            logging.info(f'SOURCE PORT RANGE | {r.source_port_range}')
            logging.info(f'SOURCE ADDR RANGE | {r.source_address_prefix}')
            logging.info(f'DEST PORT RANGE   | {r.destination_port_range}')
            logging.info(f'DEST ADDR RANGE   | {r.destination_address_prefix}')
            logging.info(f'ACTION            | {r.access}')
                
            if "-" in r.source_port_range:
                rule_src_port_range = r.source_port_range.split("-")
                rule_starting_src_port = rule_src_port_range[0]
                rule_ending_src_port = rule_src_port_range[1]
                logging.info(f'Source start port is {rule_starting_src_port}')
                logging.info(f'Source end port is {rule_ending_src_port}')
                is_source_port_range = True
                
            if "-" in r.destination_port_range:
                rule_dest_port_range = r.destination_port_range.split("-")
                rule_starting_dest_port = rule_dest_port_range[0]
                rule_ending_dest_port = rule_dest_port_range[1]
                logging.info(f'Dest start port is {rule_starting_dest_port}')
                logging.info(f'Dest end port is {rule_ending_dest_port}')
                is_dest_port_range = True
                
            if ((src_port_field_check == True) and (source_port in r.source_port_range) or (source_port == '*' and r.source_port_range == '*') or (is_source_port_range == True and source_port >= rule_starting_src_port and source_port <= rule_ending_src_port)):
                logging.info(f'Rule {rule_name} Source port match, incrementing hit counter','\n')
                match_counter = match_counter + 1
            
            if ((src_address_scope_field_check == True) and (source_scope in r.source_address_prefix) or (source_scope == '0.0.0.0/0' and r.source_address_prefix == '*')):
                logging.info(f'Rule {rule_name} Source address scope match, incrementing hit counter')
                match_counter = match_counter + 1
            
            if ((dest_port_field_check == True) and (destination_port in r.destination_port_range) or (destination_port == '*' and r.destination_port_range == '*') or (is_dest_port_range == True and destination_port >= rule_starting_dest_port and destination_port <= rule_ending_dest_port)):
                logging.info(f'Rule {rule_name} Destination port range match, incrementing hit counter')
                match_counter = match_counter + 1
            
            if ((dest_address_scope_field_check == True) and (destination_scope in r.destination_address_prefix) or (destination_scope == '0.0.0.0/0' and r.destination_address_prefix == '*')):
                logging.info(f'Rule {rule_name} Destination address match, incrementing hit counter')
                match_counter = match_counter + 1
            
            if ((action_field_check == True) and (access in r.access)):
                logging.info(f'Rule {rule_name} Access match, incrementing hit counter')
                match_counter = match_counter + 1
                logging.info(f'NSG Rule field number of hits is {match_counter}')
                
            if match_counter == fields_to_match:
                logging.info(f'Based on pattern match, deleting rule ID {rule_name}')
                network_client.security_rules.delete(resource_group_name, nsg_name, rule_name)
    except CloudError as e:
        msg = f'unexpected error : {e.message}'
        logging.error(f'{__file__} - {msg}')

        return f'{msg}'
                
                