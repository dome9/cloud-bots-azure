# Bots

## delete_network_security_group

What it does: deletes the Azure Network Security Group in the finding

Usage: AUTO: delete_network_security_group

Sample GSL:    NetworkSecurityGroup should have networkAssetsStatslength()>0 

Limitations: None

## tag_virtual_machine

What it does: tags the Azure VM in the finding 

Usage: AUTO: tag_virtual_machine tag-name tag-value  

Sample GSL:   VirtualMachine should have tags contain [ ( key like ‘Prod' ) ]

Limitations: None

## virtual_machine_stop

What it does: stops the Azure VM in the finding

Usage: AUTO: virtual_machine_stop

Sample GSL:   VirtualMachine should have tags contain [ ( key like ‘Prod' ) ]

Limitations: None

## modify_network_security_group_scope_by_port

What it does: Change network security group scope by a given port. Scope can be list of ip addresses with ',' between. example: '192.168.99.0/24,10.0.0.0/24,44.66.0.0/24'. Direction can be: source or destination. Bot will remove Any from direction.

Access can be : Allow or Deny

Example: AUTO: modify_network_security_group_scope_by_port 556 source 10.0.0.0/24,172.16.0.1/32,168.243.22.0/23 Allow

Usage: AUTO: modify_network_security_group_scope_by_port <port> <direction> <scope> <access>

Sample GSL: NetworkSecurityGroup should have inboundRules contain [ destinationPort=22 and source='0.0.0.0/0' ]

Limitations: None

## storage_account_enable_https_traffic_only

What it does: Enable storage account secure transfer required configuartion

Example: AUTO: storage_account_enable_https_traffic_only

Limitations: None

## delete_network_security_group_single_rule

What it does: Delete network security group rule. Deletion will be preformed by given destination port, destination scope, source port, source scope and access. In case you don't want to use specific destination you need to fill '-' in the specific field.

Access can be : Allow or Deny

Usage: AUTO: delete_network_security_group_single_rule <destination port> <destination scope> <source port> <source scope> <access>

Example 1: AUTO: delete_network_security_group_single_rule 556 10.0.0.0/24 22 0.0.0.0/2 Allow

Example 2: AUTO: delete_network_security_group_single_rule 556 10.0.0.0/24 - - Allow

Example 3: AUTO: delete_network_security_group_single_rule - - 22 0.0.0.0/2 Deny

Limitations: None