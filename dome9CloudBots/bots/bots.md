# Bots

## sql_disable_public_access

What it does: Sets "Deny public network access" Azure SQL flag to "Yes" and "Minimal TLS Version" to specified optional value

Usage: sql_disable_public_access min-tls-version - supported values are tls_10, tls_11, tls_12

Example: sql_disable_public_access tls_12

Limitations: None

## sql_enable_azure_ad_authentication

What it does: Sets an Azure SQL Server to use Azure AD authentication for Administrators

Usage: sql_enable_azure_ad_authentication azure-ad-admin-email azure-ad-admin-sid azure-ad-tenant-id

Example: sql_enable_azure_ad_authentication sqladmin@mytenant.onmicrosoft.com 2be17144-2741-1111-ce5e-614a7bb5a9b5 12aa321e-a741-11b8-b5e9-52d834f3d0c0

Limitations: None

## storage_account_disable_public_network_access

What it does: Sets an Azure storage account to allow access only from VNet traffic (changes *"Allow access from all networks"* to disabled)

Usage: storage_account_disable_public_network_access <vnet resource group> <vnet> <subnet>
  
Example usage: storage_account_disable_public_network_access my-resource-group my-vnet my-subnet

Limitations: Requires an existing service endpoint connection between the chosen VNet and the Storage service. 

## postgres_enable_connection_throttling

What it does: Enables connection throttling on an Azure PostgreSQL server to help prevent DoS attacks

Usage:  postgres_enable_connection_throttling

Sample GSL: PostgreSQL should have logsConfiguration with [ value='ON'] where name='connection_throttling'
                          
Limitations: None

## postgres_enable_log_connections

What it does: Enables connection logging on an Azure PostgreSQL server to help prevent unauthorised access

Usage:  postgres_enable_log_connections

Sample GSL: PostgreSQL where logsConfiguration contain [ name='log_connections' ] should have logsConfiguration with [ value='on' ]
                          
Limitations: None

## postgres_enable_log_disconnections

What it does: Enables disconnection logging on an Azure PostgreSQL server to log end of a session, including duration, which in turn generates query and error logs. 

Usage:  postgres_enable_log_disconnections

Sample GSL: PostgreSQL where logsConfiguration contain [ name='log_disconnections' ] should have logsConfiguration with [ value='ON' ]                        

Limitations: None

## postgres_enable_log_duration

What it does: Enables connection duration logging on an Azure PostgreSQL server to log end of a session 

Usage:  postgres_enable_log_duration

Sample GSL: PostgreSQL where logsConfiguration contain [ name='log_duration' ] should have logsConfiguration with [ value='ON' ]              

Limitations: None

## postgres_enable_log_retention_days_7

What it does: Enables log retention on an Azure PostgreSQL server to the maximum value of 7 days

Usage:  postgres_enable_log_retention_days_7

Sample GSL: PostgreSQL should have logsConfiguration contain [ name='log_retention_days'  and value in ('7')]
                          
Limitations: None

## postgres_enforce_ssl_connection

What it does: Enables forcing TLS connections to an Azure PostgreSQL server. Enforcing SSL connections between database server and client applications helps protect against "man in the middle" attacks by encrypting the data stream between the server and application.

Usage:  postgres_enforce_ssl_connection

Sample GSL: PostgreSQL should have sslEnforcement='Enabled'
                          
Limitations: None

## postgres_enforce_ssl_connection_tls_12

What it does: Enables forcing TLS 1.2 connections to an Azure PostgreSQL server. Enforcing SSL connections between database server and client applications helps protect against "man in the middle" attacks by encrypting the data stream between the server and application. TLS 1.2 is the strongest current encryption available for database connections.

Usage:  postgres_enforce_ssl_connection_tls_12

Sample GSL: PostgreSQL should have sslEnforcement='Enabled'

Limitations: None

## sql_enable_data_encryption

What it does: Enables Transparent Data Encryption (TDE) on an Azure SQL server. Transparent data encryption helps protect against the threat of malicious activity by performing real-time encryption and decryption of the database, associated backups, and transaction log files at rest without requiring changes to the application.

Usage:  sql_enable_data_encryption

Sample GSL: SQLDB should have encryption.status='Enabled'
                          
Limitations: None

## delete_network_security_group

What it does: deletes the Azure Network Security Group in the finding

Usage:  delete_network_security_group

Sample GSL:    NetworkSecurityGroup should have networkAssetsStatslength()>0 

Limitations: None

## tag_virtual_machine

What it does: tags the Azure VM in the finding 

Usage:  tag_virtual_machine tag-name tag-value  

Sample GSL:   VirtualMachine should have tags contain [ ( key like ‘Prod' ) ]

Limitations: None

## virtual_machine_stop

What it does: stops the Azure VM in the finding

Usage:  virtual_machine_stop

Sample GSL:   VirtualMachine should have tags contain [ ( key like ‘Prod' ) ]

Limitations: None

## modify_network_security_group_scope_by_port

What it does: Change network security group scope by a given port. Scope can be list of ip addresses with ',' between. example: '192.168.99.0/24,10.0.0.0/24,44.66.0.0/24'. Direction can be: source or destination. Bot will remove Any from direction.

Access can be : Allow or Deny

Example:  modify_network_security_group_scope_by_port 556 source 10.0.0.0/24,172.16.0.1/32,168.243.22.0/23 Allow

Usage:  modify_network_security_group_scope_by_port <port> <direction> <scope> <access>

Sample GSL: NetworkSecurityGroup should have inboundRules contain [ destinationPort=22 and source='0.0.0.0/0' ]

Limitations: None

## storage_account_enable_https_traffic_only

What it does: Enable storage account secure transfer required configuartion

Example:  storage_account_enable_https_traffic_only

Limitations: None

## delete_network_security_group_single_rule

What it does: Delete network security group rule. Deletion will be preformed by given destination port, destination scope, source port, source scope and access. In case you don't want to use specific destination you need to fill '-' in the specific field.

Access can be : Allow or Deny

Usage:  delete_network_security_group_single_rule <destination port> <destination scope> <source port> <source scope> <access>

Example 1:  delete_network_security_group_single_rule 556 10.0.0.0/24 22 0.0.0.0/2 Allow

Example 2:  delete_network_security_group_single_rule 556 10.0.0.0/24 - - Allow

Example 3:  delete_network_security_group_single_rule - - 22 0.0.0.0/2 Deny

Limitations: None
