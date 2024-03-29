import logging


class EntitiesTypes:
    COSMOS_DB_ACCOUNT = 'CosmosDbAccount'
    VIRTUAL_MACHINE = 'VirtualMachine'
    STORAGE_ACCOUNT = 'StorageAccount'
    SQL_DB = 'SQLDB'
    REDIS_CACHE = 'RedisCache'
    SQL_SERVER = 'SQLServer'
    NETWORK_SECURITY_GROUP = 'NetworkSecurityGroup'


def get_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg


def are_credentials_and_subscription_exists(subscription_id, credentials):
    if not subscription_id or not credentials:
        return False
    return True


def is_correct_type(expected_type, given_type):
    return expected_type == given_type
