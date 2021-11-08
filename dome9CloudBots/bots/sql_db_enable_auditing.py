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

if __name__ == '__main__':
    pass