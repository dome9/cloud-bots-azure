import unittest
import os
import json
import dome9CloudBots.handle_event

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

    @unittest.skipIf(IS_EXTERNAL_TEST == '1', 'Testing externally')
    def test_local(self):
        print('local')
        pass


if __name__ == '__main__':
    unittest.main()
