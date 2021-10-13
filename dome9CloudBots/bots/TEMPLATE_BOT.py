# This file use as template for writting new bots.
# Program flow in general :
# Azure CloudBots is trigger by webhook, the main function in init.py is triggered first, it call the handle_event that iterate the bots from compliance tags section
# and run them one by one. Bot run start from it run_action function
# run_action recive credentials as parameter, which are generated from the global variabled CLIENT_ID, SECRET and TENANT, entity and rule that are recived from Dome9 finding and params.
# Params are optional and are available by need. Example: AUTO: some_bot param1 param2

# Basic import for Bot execution. you should import the right Azure SDK library for your bot
from msrestazure.azure_exceptions import CloudError
from azure.core.exceptions import HttpResponseError
import logging
import dome9CloudBots.bots_utils

def run_action(credentials ,rule, entity, params):
    logging.info(f'{__file__} - run_action started')
    # Gets the relevant subscription from Dome9 finding
    subscription_id = entity.get('accountNumber')

    # Make sure you have the relevant subscription and credentials to perform action in Azure
    if not dome9CloudBots.bots_utils.are_credentials_and_subscription_exists(subscription_id, credentials):
        error_msg = dome9CloudBots.bots_utils.get_credentials_error()
        return error_msg

    # Generate the suitable Azure client object for API calls
    # Example : compute_client = ComputeManagementClient(credentials, subscription_id)
    output_msg = ''
    try:
        # Execute Azure API call
        # Example : compute_client.virtual_machines.power_off(group_name, vm_name)
        # If there is no exception the API call succeeded and create message that summarize bot execution
        # Example:
        id = entity.get('id')
        msg = f'Virtual machine was stopped. id: {id}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg
        # Return the message, this is the Bot message in the remediation output
        return f'{msg}'

    except HttpResponseError as e:
        # If there is exception the API call failed so create message summarize the failure
        msg = f'Failed to stop virtual machine : {e.message}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    except Exception as e:
        # Catch here global exceptions
        msg = f'Unexpected error : {e}'
        logging.info(f'{__file__} - {msg}')
        output_msg += msg

    return output_msg


# The bot return value is the Bot_message in the rule violation found in the remediation output
# It is highly important to add as many relevant logs as possible
