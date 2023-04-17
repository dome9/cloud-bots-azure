# download azure sdk
# in cmd run:
# az login

from azure.cli.core import get_default_cli
import unittest
from unittest.mock import patch
import os
import json
import dome9CloudBots.handle_event
import dome9CloudBots.bots.cosmos_db_account_add_tag
import dome9CloudBots.send_logs_api_gateway as send_logs_to_api_gateway

BOT_NAME = 'cosmos_db_account_add_tag'


message = r'''{
	"status": "Failed",
	"findingKey": "PKn4JEIxyPopzyZJ+ieCpg",
	"reportTime": "2023-02-09T01:15:28Z",
	"rule": {
		"name": "Overprivileged IamRole",
		"complianceTags": ""
	},
	"account": {
		"id": "838321622243",
		"name": "D9-SB-PREQA",
		"vendor": "AZURE",
		"dome9CloudAccountId": "90c256e3-5b10-4e92-b5e1-551590b5ed21"
	},
	"region": "us-east-1",
	"entity": {
		"id": "i-0de503b3ab201eefa",
		"vpc": {
			"id": "vpc-063e475f153d6db07"
		},
		"arn": "arn:aws:iam::941298424820:role/AwsInternetGateway-metric-role-qa"
	},
	"remediationActions": ["cosmos_db_account_add_tag"],
	"logsHttpEndpoint": "https://03nlnc41gk.execute-api.us-east-1.amazonaws.com/remediation/feedback",
	"logsHttpEndpointKey": "V274YHPSVG9gr3BxsHoN6IwEQ06ZloS6lxOX2hc3",
	"logsHttpEndpointStreamName": "remediation_feedback",
	"logsHttpEndpointStreamPartitionKey": "1",
	"executionId": "2914b53f-f785-4a7a-b616-32fe9326d39b",
	"dome9AccountId": "39801",
	"compliance_tags": []
}
'''

def test_rotem():
    entity = json.loads(message)
    output_message = {}
    export_results = dome9CloudBots.handle_event(entity, output_message)
    send_logs_to_api_gateway.send_logs_api_gateway(output_message)

if __name__ == '__main__':
    test_rotem()