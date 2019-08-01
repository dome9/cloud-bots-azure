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

Example: AUTO: modify_network_security_group_scope_by_port 556 source 10.0.0.0/24,172.16.0.1/32,168.243.22.0/23

Usage: AUTO: modify_network_security_group_scope_by_port <port> <direction> <scope>

Sample GSL: NetworkSecurityGroup should have inboundRules contain [ destinationPort=22 and source='0.0.0.0/0' ]

Limitations: None
