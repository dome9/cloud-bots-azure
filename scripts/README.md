# CloudBots Scripts

## Update CloudBots Function App

**What the script does**

Updates an existing CloudBots Function App. After running this script, your Function App will be up-to-date with the master branch of this repository.

**Prerequisites**

1. [Python 3](https://www.python.org/downloads/)
2. [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools)

**Usage**

In order to use the script, run this commands in your terminal:
```
git clone https://github.com/dome9/cloud-bots-azure.git
python cloud-bots-azure\scripts\update_function_app.py
```

**Script Explanation**

* *Adding custom CloudBots*

    The script will first ask you if you want to add files to the Function App. If you have any custom CloudBots, press 'y' and choose the files you want to add.
    The default location to adding files is the 'dome9CloudBots/bots' directory. The script will give you the option to choose another location if you want to (for example, to add a custom configuration file).

* *Function App name*
    
    You will need to provide the name of the CloudBots Function App you want to update.

* *Deleting cloned files*

    The script will ask you if you want to delete the files you cloned earlier. Press 'y' if you want the files to be deleted.

