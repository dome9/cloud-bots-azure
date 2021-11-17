# What it does: Disables non-SSL access for Redis Cache
# Usage: redis_cache_ssl_only
# Example: redis_cache_ssl_only
# Limitations: None
# Permissions: Microsoft.Cache/redis/write, Microsoft.Cache/redis/read
# Last checked 15/11

from azure.core.exceptions import HttpResponseError
from azure.mgmt.redis import RedisManagementClient
import logging
import dome9CloudBots.bots_utils 


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - run_action started')

    logging.info(f'{__file__} - checking if type is correct')
    entity_type = entity.get('type')
    if not dome9CloudBots.bots_utils.is_correct_type(dome9CloudBots.bots_utils.EntitiesTypes.REDIS_CACHE,
                                                     entity_type):
        error_msg = f'Error! entity type is not RedisCache'
        logging.error(f'{__file__} - {error_msg}')
        raise TypeError(error_msg)

    try:
        resource_group, subscription_id, redis_cache_name = extract_data_from_entity(entity)
    except KeyError as e:
        error_msg = f'Error! missing info {e}'
        logging.error(f'{__file__} - {error_msg}')
        raise KeyError(error_msg)

    logging.info(f'{__file__} - checking if credentials exists')
    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        logging.error(f'{__file__} - {error_msg}')
        raise ValueError(error_msg)

    try:
        disable_non_ssl_port(credentials, subscription_id, resource_group, redis_cache_name)
    except HttpResponseError as e:
        error_msg = f'Failed to disable non-SSL access to Redis Cache - {redis_cache_name}: {e.message}'
        logging.error(f'{__file__} - {error_msg}')
        raise Exception(error_msg)

    output_msg = f'Successfully disabled non-SSL access to Redis Cache - {redis_cache_name}'
    logging.info(f'{__file__} - {output_msg}')

    return output_msg


def disable_non_ssl_port(credentials, subscription_id, resource_group, redis_cache_name):
    redis_cache = RedisManagementClient(credentials, subscription_id)
    redis_cache.redis.update(resource_group, redis_cache_name, parameters={
        'enable_non_ssl_port': False
    })


def extract_data_from_entity(entity):
    redis_cache_name = entity['name']
    subscription_id = entity['accountNumber']
    resource_group = entity['resourceGroup']['name']
    return resource_group, subscription_id, redis_cache_name
