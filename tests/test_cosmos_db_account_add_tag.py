import unittest
from unittest.mock import patch
import os
import json
import dome9CloudBots.handle_event
import dome9CloudBots.bots.cosmos_db_account_add_tag

IS_EXTERNAL_TEST = os.getenv('IS_EXTERNAL_TEST', '0')
REAL_ENTITIES_FOLDER = os.getenv('REAL_ENTITIES_FOLDER')
BOT_NAME = 'cosmos_db_account_add_tag'


class TestCosmosDbAccountAddTag(unittest.TestCase):

    # ************************** External Tests *******************************

    @unittest.skipIf(IS_EXTERNAL_TEST == '0', 'Testing locally')
    def test_external_with_default_tags(self):
        entity_path = REAL_ENTITIES_FOLDER + '/entity_' + BOT_NAME + '_with_default_tags'
        with open(entity_path, 'r') as read_file:
            entity = read_file.read()
        entity = json.loads(entity)
        dome9CloudBots.handle_event(entity, {})

    @unittest.skipIf(IS_EXTERNAL_TEST == '0', 'Testing locally')
    def test_external_no_current_tags(self):
        entity_path = REAL_ENTITIES_FOLDER + '/entity_' + BOT_NAME + '_no_current_tags'
        with open(entity_path, 'r') as read_file:
            entity = read_file.read()
        entity = json.loads(entity)
        dome9CloudBots.handle_event(entity, {})

    # ************************** Local Tests *******************************

    def setUp(self):
        pass

    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.CosmosDBManagementClient')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.get_cosmos_db_account')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.add_tag_to_cosmos_db_account')
    @unittest.skipIf(IS_EXTERNAL_TEST == '1', 'Testing externally')
    def test_local_with_default_tags(self, add_tag_to_cosmos_db_mock, get_cosmos_db_mock, cosmos_db_client_mock):
        entity_path = 'demo_entities/' + BOT_NAME + '/cosmos_db_account_default.json'
        with open(entity_path, 'r') as read_file:
            entity = read_file.read()
        entity = json.loads(entity)
        dome9CloudBots.bots.cosmos_db_account_add_tag.run_action('None', None, entity, ['test-k', 'test-v'])

    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.CosmosDBManagementClient')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.get_cosmos_db_account')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.add_tag_to_cosmos_db_account')
    @unittest.skipIf(IS_EXTERNAL_TEST == '1', 'Testing externally')
    def test_local_incorrect_type(self, add_tag_to_cosmos_db_mock, get_cosmos_db_mock, cosmos_db_client_mock):
        entity_path = 'demo_entities/' + BOT_NAME + '/cosmos_db_account_incorrect_type.json'
        with open(entity_path, 'r') as read_file:
            entity = read_file.read()
        entity = json.loads(entity)
        with self.assertRaisesRegex(TypeError, "Error! entity type is not Cosmos DB Account"):
            dome9CloudBots.bots.cosmos_db_account_add_tag.run_action('None', None, entity, ['test-k', 'test-v'])

    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.CosmosDBManagementClient')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.get_cosmos_db_account')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.add_tag_to_cosmos_db_account')
    @unittest.skipIf(IS_EXTERNAL_TEST == '1', 'Testing externally')
    def test_local_missing_credentials(self, add_tag_to_cosmos_db_mock, get_cosmos_db_mock, cosmos_db_client_mock):
        entity_path = 'demo_entities/' + BOT_NAME + '/cosmos_db_account_default.json'
        with open(entity_path, 'r') as read_file:
            entity = read_file.read()
        entity = json.loads(entity)
        with self.assertRaisesRegex(ValueError, "Error! Subscription id or credentials are missing\."):
            dome9CloudBots.bots.cosmos_db_account_add_tag.run_action(None, None, entity, ['test-k', 'test-v'])

    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.CosmosDBManagementClient')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.get_cosmos_db_account')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.add_tag_to_cosmos_db_account')
    @unittest.skipIf(IS_EXTERNAL_TEST == '1', 'Testing externally')
    def test_local_too_many_params(self, add_tag_to_cosmos_db_mock, get_cosmos_db_mock, cosmos_db_client_mock):
        entity_path = 'demo_entities/' + BOT_NAME + '/cosmos_db_account_default.json'
        with open(entity_path, 'r') as read_file:
            entity = read_file.read()
        entity = json.loads(entity)
        with self.assertRaisesRegex(ValueError, "Error! Incorrect number of params \(expected 2\)"):
            dome9CloudBots.bots.cosmos_db_account_add_tag.run_action('None', None, entity, ['test-k', 'test-v', 'test'])

    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.CosmosDBManagementClient')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.get_cosmos_db_account')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.add_tag_to_cosmos_db_account')
    @unittest.skipIf(IS_EXTERNAL_TEST == '1', 'Testing externally')
    def test_local_no_params(self, add_tag_to_cosmos_db_mock, get_cosmos_db_mock, cosmos_db_client_mock):
        entity_path = 'demo_entities/' + BOT_NAME + '/cosmos_db_account_default.json'
        with open(entity_path, 'r') as read_file:
            entity = read_file.read()
        entity = json.loads(entity)
        with self.assertRaisesRegex(ValueError, "Error! Incorrect number of params \(expected 2\)"):
            dome9CloudBots.bots.cosmos_db_account_add_tag.run_action('None', None, entity, [])

    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.CosmosDBManagementClient')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.get_cosmos_db_account')
    @patch('dome9CloudBots.bots.cosmos_db_account_add_tag.add_tag_to_cosmos_db_account')
    @unittest.skipIf(IS_EXTERNAL_TEST == '1', 'Testing externally')
    def test_local_missing_info(self, add_tag_to_cosmos_db_mock, get_cosmos_db_mock, cosmos_db_client_mock):
        entity_path = 'demo_entities/' + BOT_NAME + '/cosmos_db_account_missing_info.json'
        with open(entity_path, 'r') as read_file:
            entity = read_file.read()
        entity = json.loads(entity)
        with self.assertRaisesRegex(KeyError, "Error! missing info .*"):
            dome9CloudBots.bots.cosmos_db_account_add_tag.run_action('None', None, entity, ['test-k', 'test-v'])


if __name__ == '__main__':
    unittest.main()
