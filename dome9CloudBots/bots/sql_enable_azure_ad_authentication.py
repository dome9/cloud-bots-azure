# What it does: Sets an Azure SQL Server to use Azure AD authentication for Administrators
# Usage: sql_enable_azure_ad_authentication <azure-ad-admin-email> <azure-ad-admin-sid> <azure-ad-tenant-id>
# Usage: Example sql_enable_azure_ad_authentication sqladmin@mytenant.onmicrosoft.com 2be17144-2741-1111-ce5e-614a7bb5a9b5 12aa321e-a741-11b8-b5e9-52d834f3d0c0
# Limitations: None
# Updated 8/2/21

import logging
from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.sql.models import ServerAzureADAdministrator, AdministratorType
import dome9CloudBots.bots_utils


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - ${run_action.__name__} started')
    azure_ad_admin_name, azure_ad_user_sid, tenant = params
    group_name = entity.get('resourceGroup', {}).get('name')
    subscription_id = entity.get('accountNumber')
    server_name = entity.get('name')
    admin_name = 'activeDirectory'
    admin_params = 'administrator_type'
    logging.info(
        f'{__file__} - subscription_id : {subscription_id} - group_name : {group_name} - server_name : {server_name} - azure_ad_admin : {azure_ad_admin_name} - azure_user_sid : {azure_ad_user_sid} - tenant : {tenant}')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    try:
        sql_client = SqlManagementClient(credentials, subscription_id)
        sql_client.server_azure_ad_administrators.begin_create_or_update(group_name, server_name, admin_name, 
            ServerAzureADAdministrator(administrator_type=AdministratorType("ActiveDirectory"),login=azure_ad_admin_name, sid=azure_ad_user_sid, tenant_id=tenant))  
        msg = f'Azure AD Administrator authentication enabled successfully on database server: {server_name}'
        logging.info(f'{__file__} - {msg}')
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'Unexpected error : {e.message}'
        logging.info(f'{__file__} - {msg}')
        return msg
    