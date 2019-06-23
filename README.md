<<<<<<< HEAD
# Azure CloudBots

# Overview

# Flow Diagram

![Flow Diagram](docs/pictures/Azure-CloudBots-Flow-Diagram.png)
=======
# CloudBots - Azure EA


## What are Dome9 CloudBots?

Cloud-Bots is an auto remediation solution for Azure, built on top of the
CloudGuard Dome9 Continuous Compliance capabilities.

They can also be used standalone, without Dome9, to remedy issues in AWS
accounts. Details are included how to configure and trigger them.

## The Bots

Refer to [this](HttpTrigger/bots/Bots.md) file for a list of the bots, what each one
does, and an example of a rule that could be used to trigger it.

# Onboarding

## Setup your Azure account for CloudBots

Currently we ate supporting only manual installation, automatic deploy will be available in the next version.

1. Install Dependencies<br />
    A) [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) and login to your Azure account<br />
    B) Install [Docker](https://www.docker.com)<br />
    C) Install [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools)<br />
    D) Install [Python 3.6.X](https://www.python.org/)<br />
    
2. Create Azure App Registration:<br />
    A) In Azure portal go to Home -> App registrations and click *New registration*<br />
    B) Enter make-seance name such as 'dome9CloudBots' and click *Register*<br />
    C) Copy and securely save the *Application (client) ID* and *Directory (tenant) ID*<br /> 
    D) Go to 'Certificates & secrets' in the inner left side menu and click on *New client secret* button and click *Add*<br />
    E) Securely save the created *Client secrets*<br />

3. Create SendGrid - use for sending output remediation by Email (Optional)<br />
    A) Go to Home -> SendGrid Accounts<br />
    B) Click *Add* button and fill the signup form<br />
    C) After creation process completed click on the created item and click *Manage*<br />
    D) In the SendGrip Portal left side menu go to Settings -> API Keys and click *Create API Key*<br />
    E) Give make-seance name 'dome9CloudBots', *Full Access* and click *Create & View*<br />
    F) Securely save the created *API Key*<br />

4. Assign Roles<br />
    A) Go to Home -> Subscriptions<br />
    B) Click on one Subscription that will use for CloudBots<br />
    C) Click *Access control (IAM)* at the inner left side menu<br />
    D) Click *Add* -> *Add role assignment*<br />
    E) Fill the following form:<br />
        - Role: Contributor<br />
        - Select: select the App Registration from step 3.B<br />
    F) Click *Save*<br />
    G) Repeat all of the above for each desired target Subscription<br />

5. Create Azure Function App<br />
    A) Go to Home -> Function App<br />
    B) Click *Add* button<br />
    C) Fill the form with the following data (values that are not mention leave the default): <br />
        - App name: 'dome9CloudBots'<br />
        - Resource Group: use the name from step 3.B<br />
        - OS: Linux<br />
        - Runtime Stack: Python<br />
    D) Click create *Create*<br />
    
6. Deployment<br />
    A) Clone CloudBots Azure code from [GitHub](https://github.com/Dome9/cloud-bots-azure)<br />
    B) Navigate to the locally cloned CloudBots directory and write the following command:<br />
    ```
    func init --docker
    ```
    C) Select Python<br />
    D) Deploying the code to the remote Function App (this could take a while). Run the following command (${functionAppName} should be replace with the name that was given from step 5.C):
    ```
    func azure functionapp publish ${functionAppName} --build-native-deps
    ```
    E) On Azure portal navigate to the Function App and go to *Configuration*<br />
    F) Set environment variables - Click *New application settings* and repeat it for each item bellow<br />
    
       Name: SECRET
       Value: enter the value from step 2.E
          
       Name: TENANT
       Value: enter the value from step 2.C
                
       Name: CLIEND_ID
       Value: enter the value from step 2.C

       Name: SEND_GRID_API_CLIENT
       Value: enter the value from step 2.F
          
       Name: OUTPUT_EMAIL
       Value: enter email address          
          
       Name: SEND_LOGS
       Value: True/False
     G) Click *Save*           
          
# Setup your Dome9 account

On Dome9 you must add remediation tags to rules in a compliance ruleset

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
Continuous Compliance policy to run the ruleset, and send findings to
the SNS.

1.  Navigate to the **Policies** page in the Compliance & Governance
    menu.
2.  Click **ADD POLICY** (on the right).
3.  Select the account from the list, then click **NEXT**, this will be the one account in which the bots are deployed.
4.  Select the ruleset from the list, then click **NEXT**.
5.  Click **ADD NOTIFICATION**.
6.  Select *Webhook integration* and enter the HTTP from the Function App and then click **SAVE**.

**Note:** Dome9 will send event messages to the SNS for new findings. To
send events for previous findings, follow these steps:

1.  Navigate to the **Policies** page.
2.  Find the ruleset and account in the list, and hover over the right
    of the row, then click on the *Send All Alerts* icon.
3.  Select the *SNS* Notification Type option, and the Notification
    Policy (the one created above), then click **SEND**. Dome9 will send
    event messages to the SNS for findings.

# Use the CloudBots without Dome9

You can use the CloudBots without a Dome9 account. In this case you must
send messages to the SNS for each event that requires remediation. The
message should have the following format:

    {
      "reportTime": "2018-03-20T05:40:42.043Z",
      "rule": {
        "name": "<name for rule>",
        "complianceTags": "AUTO: <bot-name>"
      },
      "status": "Failed",
      "account": {
        "id": "************"
      },
      "entity": {
        "accountNumber": "************",
        "id": "i-*****************",
        "name": "************",
        "region": "us_west_2",
      }
    }

where *account: id* and *accountNumber* is your Azure account number
*status* is marked *Failed*
*entity: id* is the id for the entity that failed the rule
>>>>>>> master
