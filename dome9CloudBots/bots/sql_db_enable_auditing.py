from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import ClientSecretCredential
from azure.mgmt.sql import SqlManagementClient


if __name__ == '__main__':
    CLIENT_ID = 'de3e976b-819e-4aa4-89ca-dffd8a409468'
    DIRECTORY_ID = '741aca19-10ab-4d3d-9e7c-43b5ff76773c'
    CLIENT_SECRET = 'LQW7Q~GdmjswW~rATCcNnXQtB6q4YnsvBiEl5'

    credentials = ClientSecretCredential(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            tenant_id=DIRECTORY_ID
        )

    subscription_id = '66de47d2-4c17-4a17-bb9d-3b3f0cac31f0'

    monitor = MonitorManagementClient(credentials, subscription_id)
    sql_client = SqlManagementClient(credentials, subscription_id)

    resource_uri = '/subscriptions/66de47d2-4c17-4a17-bb9d-3b3f0cac31f0/resourceGroups/Tests/providers/Microsoft.Sql/servers/bots-playground-sql-server/databases/sql_db_enable_auditing'
    name = 'test-diagnostic-settings-sql-db'
    event_hub_name = 'test-event-hub'
    metrics = [{'category': "Basic", 'enabled': False, 'retention_policy': {'days': 0, 'enabled': False}, 'timeGrain': None}]
    logs = [{
      "category": "SQLSecurityAuditEvents",
      "categoryGroup": None,
      "enabled": True,
      "retentionPolicy": {
        "days": 0,
        "enabled": False
      }
    }]
    ws = '/subscriptions/66de47d2-4c17-4a17-bb9d-3b3f0cac31f0/resourcegroups/tests/providers/microsoft.operationalinsights/workspaces/sql-db-enable-auditing-ws'
    auth_rule = '/subscriptions/66de47d2-4c17-4a17-bb9d-3b3f0cac31f0/resourceGroups/Tests/providers/Microsoft.EventHub/namespaces/sql-db-enable-auditing/authorizationRules/RootManageSharedAccessKey'

    storage_endpoint = 'https://testsqldbenableauditing.blob.core.windows.net/'
    # monitor.diagnostic_settings.create_or_update(resource_uri, name, parameters={'event_hub_name': event_hub_name, 'metrics': metrics, 'logs': logs})
    ds = monitor.diagnostic_settings.create_or_update(resource_uri, name, parameters={
                                                                                 'event_hub_name': event_hub_name,
                                                                                 'event_hub_authorization_rule_id': auth_rule,
                                                                                 'logs': logs,
                                                                                 'metrics': metrics})

    # storage_account_id = '/subscriptions/66de47d2-4c17-4a17-bb9d-3b3f0cac31f0/resourceGroups/Tests/providers/Microsoft.Storage/storageAccounts/testsqldbenableauditing'
    # ds = monitor.diagnostic_settings.create_or_update(resource_uri, name, parameters={'storage_account_id': storage_account_id,
    #                                                                                   'logs': logs,
    #                                                                                   'metrics': metrics})

    # storage_account_id = '/subscriptions/66de47d2-4c17-4a17-bb9d-3b3f0cac31f0/resourceGroups/Tests/providers/Microsoft.Storage/storageAccounts/testsqldbenableauditing'
    # ds = monitor.diagnostic_settings.create_or_update(resource_uri, name,
    #                                                   parameters={'workspace_id': ws,
    #                                                               'logs': logs,
    #                                                     \          'metrics': metrics})

    parameters = {
        'state': 'Enabled',
        # 'storage_endpoint': storage_endpoint,
        # 'storage_account_access_key': 't7eVSmGwALls6bl4amVv2i82ZSZ4YcJc6OSi48WpBpoo2NeX2VqHZIqUYQLnz2e83LCFOouYqcLldvGM647UtQ==',
        'is_azure_monitor_target_enable': 'true',
        "auditActionsAndGroups": [
            "SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP",
            "FAILED_DATABASE_AUTHENTICATION_GROUP",
            "BATCH_COMPLETED_GROUP"
        ]
    }

    policy = sql_client.database_blob_auditing_policies.create_or_update('Tests', 'bots-playground-sql-server',
                                                                         'sql_db_enable_auditing',
                                                                         parameters=parameters)

    # policy = sql_client.database_blob_auditing_policies.create_or_update('Tests', 'bots-playground-sql-server',
    #                                                                      'sql_db_enable_auditing',
    #                                                                      parameters={
    #                                                                          'storage_endpoint': storage_endpoint,
    #                                                                          'storage_account_subscription_id': subscription_id,
    #                                                                          'state': 'Enabled',
    #                                                                          "auditActionsAndGroups": [
    #                                                                              "SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP",
    #                                                                              "FAILED_DATABASE_AUTHENTICATION_GROUP",
    #                                                                              "BATCH_COMPLETED_GROUP"
    #                                                                          ],
    #                                                                      })

    print(ds)
    print(policy)

    # params: event_hub_namespace event_hub_name event_hub_authorization_rule_name storage_account_name storage_endpoint storage_account_access_key workspace_id

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
import uuid
import dome9CloudBots.bots_utils

EMPTY = '-'

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

DIAGNOSTIC_SETTINGS_PARAMETERS = {
    'logs': LOGS,
    'metrics': METRICS
}

ENABLE_AUDIT_PARAMETERS = {
    'state': 'Enabled',
    'is_azure_monitor_target_enable': True,
    'auditActionsAndGroups': [
        'SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP',
        'FAILED_DATABASE_AUTHENTICATION_GROUP',
        'BATCH_COMPLETED_GROUP'
    ]
}


def run_action(credentials, rule, entity, params):
    logging.info(f'{__file__} - run_action started')

    logging.info(f'{__file__} - checking if type is correct')
    entity_type = entity.get('type')
    if not dome9CloudBots.bots_utils.is_correct_type(dome9CloudBots.bots_utils.EntitiesTypes.SQL_DB,
                                                     entity_type):
        error_msg = f'Error! entity type is not SQL DB'
        logging.error(f'{__file__} - {error_msg}')
        raise TypeError(error_msg)

    try:
        resource_group, subscription_id, database_name, server_name = extract_data_from_entity(entity)
    except KeyError as e:
        error_msg = f'Error! missing info {e}'
        logging.error(f'{__file__} - {error_msg}')
        raise KeyError(error_msg)

    logging.info(f'{__file__} - checking if credentials exists')
    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        logging.error(f'{__file__} - {error_msg}')
        raise ValueError(error_msg)

    update_diagnostic_settings_parameters(params, resource_group, subscription_id)
    diagnostic_settings_name = generate_diagnostic_settings_name(database_name)

    try:
        logging.info(f'Trying to create Diagnostic Settings - {diagnostic_settings_name}')
        create_diagnostic_settings(credentials, subscription_id, resource_group,
                                   database_name, server_name, diagnostic_settings_name)
        logging.info(f'Successfully created Diagnostic Settings - {diagnostic_settings_name}')
    except HttpResponseError as e:
        error_msg = f'Failed to create Diagnostic Settings - {e.message}'
        logging.error(f'{__file__} - {error_msg}')
        raise Exception(error_msg)

    try:
        logging.info(f'Trying to enable audit for SQL DB: {database_name}')
        enable_audit_for_sql_sb(credentials, subscription_id, resource_group, database_name, server_name)
    except HttpResponseError as e:
        error_msg = f'Failed to enable audit for SQL DB: {database_name} - {e.message}'
        logging.error(f'{__file__} - {error_msg}')
        raise Exception(error_msg)

    output_msg = f'Successfully enabled auditing for SQL Database: {database_name}'
    logging.info(f'{__file__} - {output_msg}')

    return output_msg


def enable_audit_for_sql_sb(credentials, subscription_id, resource_group, database_name, server_name):
    sql_client = SqlManagementClient(credentials, subscription_id)
    sql_client.database_blob_auditing_policies.create_or_update(resource_group, server_name, database_name,
                                                                parameters=ENABLE_AUDIT_PARAMETERS)


def create_diagnostic_settings(credentials, subscription_id, resource_group, database_name, server_name,
                               diagnostic_settings_name):
    monitor = MonitorManagementClient(credentials, subscription_id)
    sql_db_uri = '/subscriptions/' + subscription_id + '/resourceGroups/' + resource_group + \
                 '/providers/Microsoft.Sql/servers/' + server_name + '/databases/' + database_name
    monitor.diagnostic_settings.create_or_update(sql_db_uri, diagnostic_settings_name,
                                                 parameters=DIAGNOSTIC_SETTINGS_PARAMETERS)


def generate_diagnostic_settings_name(database_name):
    return database_name + '-audit-' + uuid.uuid4().hex[:8]


def update_diagnostic_settings_parameters(params, resource_group, subscription_id):
    logging.info(f'{__file__} - trying to get params')
    try:
        event_hub_namespace, event_hub_name, event_hub_authorization_rule_name, \
            storage_account_name, storage_endpoint, storage_account_access_key, workspace_id = params
    except ValueError:
        error_msg = 'Error! Incorrect number of params (expected )'
        logging.error(f'{__file__} - {error_msg}')
        raise ValueError(error_msg)
    if is_storage_account_configured(storage_account_access_key, storage_endpoint):
        add_storage_account_parameters_to_diagnostic_settings(resource_group, storage_account_name, subscription_id)
    if is_log_analytics_configured(workspace_id):
        add_log_analytics_parameters_to_diagnostic_settings(workspace_id)
    if is_event_hub_configured(event_hub_authorization_rule_name, event_hub_name, event_hub_namespace):
        add_event_hub_parameters_to_diagnostic_settings(event_hub_authorization_rule_name, event_hub_name,
                                                        event_hub_namespace, resource_group, subscription_id)


def add_event_hub_parameters_to_diagnostic_settings(event_hub_authorization_rule_name, event_hub_name,
                                                    event_hub_namespace, resource_group, subscription_id):
    event_hub_authorization_rule_id = '/subscriptions/' + subscription_id + '/resourceGroups/' + resource_group + \
                                      '/providers/Microsoft.EventHub/namespaces/' + event_hub_namespace + \
                                      '/authorizationRules/' + event_hub_authorization_rule_name
    DIAGNOSTIC_SETTINGS_PARAMETERS['event_hub_name'] = event_hub_name
    DIAGNOSTIC_SETTINGS_PARAMETERS['event_hub_authorization_rule_id'] = event_hub_authorization_rule_id


def add_log_analytics_parameters_to_diagnostic_settings(workspace_id):
    DIAGNOSTIC_SETTINGS_PARAMETERS['workspace_id'] = workspace_id


def add_storage_account_parameters_to_diagnostic_settings(resource_group, storage_account_name, subscription_id):
    storage_account_id = '/subscriptions/' + subscription_id + '/resourceGroups/' + resource_group + \
                         '/providers/Microsoft.Storage/storageAccounts/' + storage_account_name
    DIAGNOSTIC_SETTINGS_PARAMETERS['storage_account_id'] = storage_account_id


def is_storage_account_configured(storage_account_access_key, storage_endpoint):
    return storage_endpoint != EMPTY and storage_account_access_key != EMPTY


def is_log_analytics_configured(workspace_id):
    return workspace_id != EMPTY


def is_event_hub_configured(event_hub_authorization_rule_name, event_hub_name, event_hub_namespace):
    return event_hub_namespace != EMPTY and event_hub_name != EMPTY and event_hub_authorization_rule_name != EMPTY


def extract_data_from_entity(entity):
    database_name = entity['name']
    server_name = entity['sqlServerName']
    subscription_id = entity['accountNumber']
    resource_group = entity['resourceGroup']['name']
    return resource_group, subscription_id, database_name, server_name
