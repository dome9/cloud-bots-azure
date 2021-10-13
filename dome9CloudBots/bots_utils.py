import logging


def get_credentials_error():
    msg = 'Error! Subscription id or credentials are missing.'
    logging.info(f'{__file__} - {msg}')
    return msg


def are_credentials_and_subscription_exists(subscription_id, credentials):
    if not subscription_id or not credentials:
        return False
    return True
