# from azure.mgmt.monitor import MonitorManagementClient
# from azure.identity import ClientSecretCredential
# from azure.mgmt.sql import SqlManagementClient
#
#
# if __name__ == '__main__':
#     CLIENT_ID = 'de3e976b-819e-4aa4-89ca-dffd8a409468'
#     DIRECTORY_ID = '741aca19-10ab-4d3d-9e7c-43b5ff76773c'
#     CLIENT_SECRET = 'LQW7Q~GdmjswW~rATCcNnXQtB6q4YnsvBiEl5'
#
#     credentials = ClientSecretCredential(
#             client_id=CLIENT_ID,
#             client_secret=CLIENT_SECRET,
#             tenant_id=DIRECTORY_ID
#         )
#
#     subscription_id = '66de47d2-4c17-4a17-bb9d-3b3f0cac31f0'
#
#     monitor = MonitorManagementClient(credentials, subscription_id)
#     sql_client = SqlManagementClient(credentials, subscription_id)
#
#     resource_uri = '/subscriptions/66de47d2-4c17-4a17-bb9d-3b3f0cac31f0/resourceGroups/Tests/providers/Microsoft.Sql/servers/bots-playground-sql-server/databases/sql_db_enable_auditing'
#     name = 'test-diagnostic-settings-sql-db'
#     event_hub_name = 'test-event-hub'
#     metrics = [{'category': "Basic", 'enabled': False, 'retention_policy': {'days': 0, 'enabled': False}, 'timeGrain': None}]
#     logs = [{
#       "category": "SQLSecurityAuditEvents",
#       "categoryGroup": None,
#       "enabled": True,
#       "retentionPolicy": {
#         "days": 0,
#         "enabled": False
#       }
#     }]
#     ws = '/subscriptions/66de47d2-4c17-4a17-bb9d-3b3f0cac31f0/resourcegroups/tests/providers/microsoft.operationalinsights/workspaces/sql-db-enable-auditing-ws'
#     auth_rule = '/subscriptions/66de47d2-4c17-4a17-bb9d-3b3f0cac31f0/resourceGroups/Tests/providers/Microsoft.EventHub/namespaces/sql-db-enable-auditing/authorizationRules/RootManageSharedAccessKey'
#
#     # monitor.diagnostic_settings.create_or_update(resource_uri, name, parameters={'event_hub_name': event_hub_name, 'metrics': metrics, 'logs': logs})
#     ds = monitor.diagnostic_settings.create_or_update(resource_uri, name, parameters={'event_hub_name': event_hub_name,
#                                                                                  'event_hub_authorization_rule_id': auth_rule,
#                                                                                  'logs': logs,
#                                                                                  'metrics': metrics})
#
#     policy = sql_client.database_blob_auditing_policies.create_or_update('Tests', 'bots-playground-sql-server', 'sql_db_enable_auditing',
#                                                                 parameters={
#                                                                     'is_azure_monitor_target_enabled': True,
#                                                                     'state': 'Enabled',
#                                                                     "auditActionsAndGroups": [
#                                                                         "SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP",
#                                                                         "FAILED_DATABASE_AUTHENTICATION_GROUP",
#                                                                         "BATCH_COMPLETED_GROUP"
#                                                                     ],
#                                                                 })
#
#     print(ds)
#     print(policy)

# What it does: enables auditing for SQL Database
# Usage: sql_db_enable_auditing # TODO add Params
# Example: sql_db_enable_auditing # todo add params
# Limitations: # todo add limitations
# Permissions: # todo add permissions
# Last checked 8/11/21

from azure.core.exceptions import HttpResponseError
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.monitor import MonitorManagementClient
import logging
import dome9CloudBots.bots_utils

STORAGE = 'storage'
ANALYTICS = 'analytics'
EVENT_HUB = 'event_hub'

AUDIT_TYPE_COL = 0

LOGS = [
    {
        "category": "SQLSecurityAuditEvents",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "SQLInsights",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "AutomaticTuning",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "QueryStoreRuntimeStatistics",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "QueryStoreWaitStatistics",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "Errors",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "DatabaseWaitStatistics",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "Timeouts",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "Blocks",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    },
    {
        "category": "Deadlocks",
        "categoryGroup": None,
        "enabled": True,
        "retentionPolicy": {
        "days": 0,
        "enabled": False
        }
    }
]

METRICS = [
    {
        'category': "Basic",
        'enabled': False,
        'retention_policy': {
            'days': 0,
            'enabled': False
        },
        'timeGrain': None
    },
    {
        'category': "InstanceAndAppAdvanced",
        'enabled': False,
        'retention_policy': {
            'days': 0,
            'enabled': False
        },
        'timeGrain': None
    },
    {
        'category': "WorkloadManagement",
        'enabled': False,
        'retention_policy': {
            'days': 0,
            'enabled': False
        },
        'timeGrain': None
    }
]

def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - run_action started')

    audit_type = params[AUDIT_TYPE_COL]

    if audit_type == EVENT_HUB:
        pass
    elif audit_type == ANALYTICS:
        pass
    elif audit_type == STORAGE:
        pass
    else:
        pass

    logging.info(f'{__file__} - trying to get params')
    try:
         audit_type = params
    except ValueError:
        error_msg = 'Error! Incorrect number of params (expected )'
        logging.error(f'{__file__} - {error_msg}')
        raise ValueError(error_msg)

    logging.info(f'{__file__} - checking if type is correct')
    entity_type = entity.get('type')
    if not dome9CloudBots.bots_utils.is_correct_type(dome9CloudBots.bots_utils.EntitiesTypes.SQL_DB,
                                                     entity_type):
        error_msg = f'Error! entity type is not SQL DB'
        logging.error(f'{__file__} - {error_msg}')
        raise TypeError(error_msg)

    try:
        resource_group, subscription_id, database_name = extract_data_from_entity(entity)
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

    except HttpResponseError as e:
        error_msg = f'Failed to enable auditing for SQL Database: {database_name} - {e.message}'
        logging.error(f'{__file__} - {error_msg}')
        raise Exception(error_msg)

    output_msg = f'Successfully enabled auditing for SQL Database: {database_name}'
    logging.info(f'{__file__} - {output_msg}')

    return output_msg

def extract_data_from_entity(entity):
    database_name = entity['name']
    subscription_id = entity['accountNumber']
    resource_group = entity['resourceGroup']['name']
    return resource_group, subscription_id, database_name

def create_event_hub_audit_parameters(subscription_id, resource_group, bot_params):
    try:
        event_hub_namespace, event_hub_name, event_hub_authorization_rule_name = bot_params
    except ValueError:
        error_msg = 'Error! Incorrect number of params (expected - )' # todo add expected
        logging.error(f'{__file__} - {error_msg}')
        raise ValueError(error_msg)

    event_hub_authorization_rule_id = '/subscriptions/' + subscription_id + '/resourceGroups/' + resource_group + \
                                      '/providers/Microsoft.EventHub/namespaces/' + event_hub_namespace + \
                                      '/authorizationRules/' + event_hub_authorization_rule_name

    diagnostic_setting_parameters = {
        'event_hub_name': event_hub_name,
        'event_hub_authorization_rule_id': event_hub_authorization_rule_id
    }