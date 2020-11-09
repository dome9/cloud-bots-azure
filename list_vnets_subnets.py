from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network import NetworkManagementClient

subscription_id = 'e584d070-3c5a-4a7c-8cf9-c063c5c67ee3'

def get_credentials():
    credentials = ServicePrincipalCredentials(
        client_id='0d0dbc89-fdff-43c3-91b9-867942eeeeef',
        secret='2?OvkE0OyvQf6Pk1kuWxlORikweaB]*-',
        tenant='42cd311b-d944-41a2-a0e9-32d934f3d0ca'
    )
    return credentials

def list_vnets():
    try:
        network_client = NetworkManagementClient(
            credentials,
            subscription_id
        )
