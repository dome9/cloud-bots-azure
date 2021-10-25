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
        error_msg = 'Error! missing params'
        logging.error(f'{__file__} - {error_msg}')
        return error_msg

    cosmos_db_account = entity.get('name')
    subscription_id = entity.get('accountNumber')
    resource_group = entity.get('resourceGroup', {}).get('name')

    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    output_msg = ''
    try:
        logging.info(f'{__file__} - trying to add tags to Cosmos DB Account')
        update_parameters = DatabaseAccountCreateUpdateParameters(tags={tag_key: tag_value})
        cosmosdb_client = CosmosDBManagementClient(credentials, subscription_id)
        cosmosdb_client.database_accounts.begin_create_or_update(resource_group, cosmos_db_account, update_parameters)
        msg = f'Successfully added tag to Cosmos DB Account: {cosmos_db_account}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg
        return f'{msg}'

    except HttpResponseError as e:
        msg = f'Failed to add tag to Cosmos DB Account - {cosmos_db_account} : {e.message}'
        logging.error(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg
