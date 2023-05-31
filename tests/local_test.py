import json
import dome9CloudBots.handle_event
import dome9CloudBots.bots.cosmos_db_account_add_tag
import dome9CloudBots.send_logs_api_gateway as send_logs_to_api_gateway


# Instructions to run locally:
# to run locally, first you need to log in to an azure account using this commends, it will open a window
# where you need to connect to azure:
# download azure sdk
# in cmd run:
# az login

# you also need to change get_credentials() to get your credentials temporary - do not forget to delete it before
# commenting to Git!

def test_remediation_locally():
    with open('virtual_machine_stop_example.json', 'r') as read_file:
        entity = read_file.read()
    entity = json.loads(entity)
    output_message = {}
    dome9CloudBots.handle_event(entity, output_message)
    send_logs_to_api_gateway.send_logs_api_gateway(output_message)

if __name__ == '__main__':
    test_remediation_locally()
