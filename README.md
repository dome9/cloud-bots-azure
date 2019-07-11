<p align="center">
    <a href="https://cloudbots.dome9.com">
      <img width="150" src="cloudbotslogo.svg">
    </a>
</p>

<div align="center">
    <h1><a target="_blank" href="https://cloudbots.dome9.com">CloudBots</a> is an automatic remediation solution for public cloud platforms (Azure, <a href="https://github.com/Dome9/cloud-bots" targe="_blank">AWS</a>, and <a href="https://github.com/Dome9/cloud-bots-gcp" targe="_blank">GCP</a>)</h1>
</div>

- [What are Dome9 CloudBots?](#what-are-dome9-cloudbots)
  - [Flow Diagram](#flow-diagram)
      - [The Bots](#the-bots)
  - [Onboarding](#onboarding)
      - [Setup your Azure account for
        CloudBots](#setup-your-azure-account-for-cloudbots)
      - [Multiple Accounts](#multiple-accounts)
  - [Setup your Dome9 account](#setup-your-dome9-account)
      - [Configure the rules](#configure-the-rules)
      - [Configure the Continuous Compliance
        policy](#configure-the-continuous-compliance-policy)
  - [Log Collection for
    Troubleshooting](#log-collection-for-troubleshooting)
	
## What are Dome9 CloudBots?

Cloud-Bots is an auto remediation solution for Azure, built on top of the
CloudGuard Dome9 Continuous Compliance capabilities.

They can also be used standalone, without Dome9, to remedy issues in AWS
accounts. Details are included how to configure and trigger them.

# Flow Diagram

![Flow Diagram](docs/pictures/Azure-CloudBots-Flow-Diagram.png)

## The Bots

Refer to [this](dome9CloudBots/bots/bots.md) file for a list of the bots, what each one
does, and an example of a rule that could be used to trigger it.

# Onboarding

## Setup your Azure account for CloudBots

Follow these steps to configure your Azure accounts to use Dome9 CloudBots.

1. Install Dependencies
    1.  [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest), and then login to your Azure account
    1.  [Docker](https://www.docker.com)
    1.  [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools)
    1.  [Python 3.6.X](https://www.python.org/)
    
1. Create Azure App Registration:
    1. In the Azure portal, navigate to App registrations, and the click *New registration*.
    1. Enter a name for the app (for example, *dome9CloudBots*), then click *Register*.
    1. Save the *Application (client) ID* and *Directory (tenant) ID*.
    1. Navigate to *Certificates & secrets*, from the left side menu, and click *New client secret*  and click *Add*
    1. Enter the secrets, saved in the previous step, in *Client secrets*. 

1. Create SendGrid, to be used to send remediation outputs by email (Optional)
    1. In the Azure console, navigate to *SendGrid Accounts*.
    1. Click *Add*, and complete the signup form.
    1. Select the new SendGrid account, and then click *Manage*.
    1. Select *Settings -> API Keys*, and then click *Create API Key.*
    1. Enter a name (for example, *dome9CloudBots*), select *Full Access*, then click *Create & View*.
    1. Save the key value (will be needed in a later step).

1. Assign Roles
	
    1. Navigate to Subscriptions.
    1. Select the subscription that will use the CloudBots.
    1. Select *Access control (IAM)* from the menu on the left.
    1. Click *Add* -> *Add role assignment*
    1. Complete the form, using following:
        - Role: Contributor
        - Select: select the App Registration from step 2, above.
    1. Click *Save*.
    1. Repeat these steps for each additional Subscription.

1. Create an Azure Function App
    1. Navigate to *Function App*.
    1. Click *Add*.
    1. Complete the form with the following(all other values - leave the default): 
        - App name: dome9CloudBots
        - Resource Group: use the name from step 2, above.
        - OS: Linux
        - Runtime Stack: Python
    1. Click *Create*.
    
1. Deployment
    1. Clone the CloudBots Azure code from [GitHub](https://github.com/Dome9/cloud-bots-azure)
    1. Navigate to the locally cloned CloudBots directory and run the following command:
    ```     func init --docker    ```
    1. Select *Python*.
    1. Deploy the code to the remote Function App (this could take a while). Run the following command, replacing $\{functionAppName}  with the Function App name that was given in the previous step (5 (v)):
    ```     func azure functionapp publish ${functionAppName} --build-native-deps  	```	
    1. In the Azure portal, navigate to the Function App and then to *Configuration*.
    1. Set the following environment variables.  Click *New application settings* and repeat for each item:
    
       Name: SECRET
       Value: enter the value from step 2 (v)
          
       Name: TENANT
       Value: enter the value from step 2 (iii)
                
       Name: CLIEND_ID
       Value: enter the value from step 2 (iii)

       Name: SEND_GRID_API_CLIENT
       Value: enter the value from step 3 (vi)
	   
       Name: OUTPUT_EMAIL
       Value: enter email address          
          
       Name: SEND_LOGS
       Value: True to enable logging to Dome9, False to disable logging
     1. Click *Save*.       
          
## Multiple Accounts

If you are onboarding several Azure accounts, repeat step 4 (Assign Roles), above, for each account.

		  
# Setup your Dome9 account

On Dome9 you must add remediation tags to rules in a compliance ruleset.

## Configure the rules

Follow these steps in your Dome9 account to tag the compliance rules &
rulesets to use bots as a remediation step.

1.  In the Dome9 console, navigate to the Rulesets page in the
    Compliance & Governance menu.

2.  Select the rules for which you want to add a remediation step.

3.  In the Compliance Section add a row with the following string:
    `AUTO: <bot-name> <params>` where *bot-name* is the name of the bot,
    and *params* is a list of arguments for the bot (if any).
    
    For example, `AUTO: ec2_virtual_machine_stop` will run the bot to stop an
    EC2 instance.

## Configure the Continuous Compliance policy

Once the rules in the ruleset have been tagged for remediation, set up a
Continuous Compliance policy to run the ruleset, and send findings the Azure function webhook.

1.  Navigate to the **Policies** page in the Compliance & Governance
    menu.
2.  Click **ADD POLICY** (on the right).
3.  Select the account from the list, then click **NEXT**, this will be the one account in which the bots are deployed.
4.  Select the ruleset from the list, then click **NEXT**.
5.  Click **ADD NOTIFICATION**.
6.  Select *Webhook integration* and enter the HTTP from the Function App and then click **SAVE**.

**Note:** Dome9 will send event messages to the webhook for new findings. To
send events for previous findings, follow these steps:

1.  Navigate to the **Policies** page.
2.  Find the ruleset and account in the list, and hover over the right
    of the row, then click on the *Send All Alerts* icon.
3.  Select the *webhook* Notification Type option, and the Notification
    Policy (the one created above), then click **SEND**. Dome9 will send
    event messages to the Azure function webhook.

# Log Collection for Troubleshooting

The cloudbots send log information to Dome9, that is used for troubleshooting. By default, this is enabled for all bots. You can disable this in your Azure account. Select the  function, and set the environment variable SEND_LOGS to False. This will apply to all bots in the account. By default, this is set to True, enabling logs.

Each account is controlled by the variable for the function configured in that account.