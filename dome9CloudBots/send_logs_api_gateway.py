import json
import requests
import base64
from datetime import datetime
import logging


def send_logs_api_gateway(message):
    url = message.get('logsHttpEndpoint')
    api_key = message.get('logsHttpEndpointKey')
    stream_name = message.get('logsHttpEndpointStreamName')
    stream_partition_key = message.get('logsHttpEndpointStreamPartitionKey')
    if url and api_key and stream_name and stream_partition_key:
        findingKey = message.get('findingKey')
        execution_time = datetime.now()
        dome9AccountId = message.get('dome9AccountId')
        vendor = message.get('vendor')
        account_id = message.get('accountId')
        execution_id = message.get('executionId')

        for bot in message.get('Rules violations found', []):
            if "Execution status" in bot:
                bot["ExecutionStatus"] = bot.pop("Execution status")

            if "Bot message" in bot:
                bot["BotMessage"] = bot.pop("Bot message")
            log_message = {
                "logType": "feedback",
                "dome9AccountId": dome9AccountId,
                "vendor": vendor,
                "findingKey": findingKey,
                "envCloudAccountId": account_id,
                "executionId": execution_id,
                "remediationInfo": bot,
                "executionTime": str(execution_time)
            }
            json_bytes = (json.dumps(log_message) + '\n').encode('utf-8')
            # Encode the JSON bytes as base64
            base64_bytes = base64.b64encode(json_bytes)
            # Convert the base64-encoded bytes to a string
            base64_string = base64_bytes.decode('utf-8')

            headers = {"Content-Type": "application/json", "x-api-key": api_key, 'Accept': 'application/json'}

            data = {"Data": base64_string, "PartitionKey": stream_partition_key, "StreamName": stream_name}
            try:
                response = requests.post(url, json=data, headers=headers)
            except Exception as e:
                logging.info(f'[send_logs_api_gateway]: failed to send post request. error: {str(e)}')

            if response.status_code == 200 and "SequenceNumber" in response.text and "ShardId" in response.text:
                logging.info(f'{findingKey} - bot feedback was reported successfully')
            else:
                logging.info(f'{findingKey} bot feedback Failed {response.text}')
