# TODO add description

from azure.core.exceptions import HttpResponseError
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.cosmosdb.models import DatabaseAccountCreateUpdateParameters
import logging
import dome9CloudBots.bots_utils 


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - run_action started')

    logging.info(f'{__file__} - trying to get params')
    try:
        tag_key, tag_value = params
    except ValueError:
        error_msg = 'Error! Incorrect number of params (expected 2)'
        logging.error(f'{__file__} - {error_msg}')
        raise ValueError(error_msg)

    try:
        entity_type, cosmos_db_account_name, region, resource_group, subscription_id = extract_data_from_entity(entity)
    except KeyError as e:
        error_msg = f'Error! missing info {e}'
        logging.error(f'{__file__} - {error_msg}')
        raise KeyError(error_msg)

    logging.info(f'{__file__} - checking if type is correct')
    if not dome9CloudBots.bots_utils.is_correct_type(dome9CloudBots.bots_utils.EntitiesTypes.COSMOS_DB_ACCOUNT,
                                                     entity_type):
        error_msg = f'Error! entity type is not Cosmos DB Account'
        logging.error(error_msg)
        raise Exception(error_msg)

    logging.info(f'{__file__} - checking if credentials exists')
    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        logging.error(error_msg)
        raise Exception(error_msg)

    try:
        logging.info(f'{__file__} - trying to add tags to Cosmos DB Account')
        cosmos_db_client = CosmosDBManagementClient(credentials, subscription_id)
        cosmos_db_account = get_cosmos_db_account(cosmos_db_client, cosmos_db_account_name, resource_group)
        add_tag_to_cosmos_db_account(cosmos_db_client, cosmos_db_account, region, tag_key, tag_value,
                                     resource_group, cosmos_db_account_name)

    except HttpResponseError as e:
        error_msg = f'Failed to add tag to Cosmos DB Account - {cosmos_db_account_name} : {e.message}'
        logging.error(f'{__file__} - {error_msg}')
        raise Exception(error_msg)

    output_msg = f'Successfully added tag to Cosmos DB Account: {cosmos_db_account_name}'
    logging.info(f'{__file__} - {output_msg}')

    return output_msg


def add_tag_to_cosmos_db_account(cosmos_db_client, cosmos_db_account, region, tag_key, tag_value,
                                 resource_group, cosmos_db_account_name):
    """
    not sending 'enable_multiple_write_locations' may raise:
    "Cannot update EnableMultipleWriteLocations flag and other properties at the same".
    not sending 'enable_free_tier' may raise:
    "Cannot update FreeTier property for existing account"
    """
    current_tags = cosmos_db_account.tags
    new_tags = current_tags
    new_tags[tag_key] = tag_value
    update_parameters = \
        DatabaseAccountCreateUpdateParameters(tags=new_tags,
                                              location=region,
                                              locations=cosmos_db_account.locations,
                                              enable_multiple_write_locations=cosmos_db_account.enable_multiple_write_locations,
                                              enable_free_tier=cosmos_db_account.enable_free_tier)
    cosmos_db_client.database_accounts.begin_create_or_update(resource_group, cosmos_db_account_name, update_parameters)


def get_cosmos_db_account(cosmos_db_client, cosmos_db_account_name, resource_group):
    cosmos_db = cosmos_db_client.database_accounts.get(resource_group, cosmos_db_account_name)
    return cosmos_db


def extract_data_from_entity(entity):
    entity_type = entity['type']
    region = entity['region']
    cosmos_db_account = entity['name']
    subscription_id = entity['accountNumber']
    resource_group = entity['resourceGroup']['name']
    return entity_type, cosmos_db_account, region, resource_group, subscription_id
