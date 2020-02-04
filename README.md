# A GitHub Organization Events listens Web Service



## Requirements
* Google Cloud SDK Account
    * App Engine
    * Datastore
* Python3
* Flask
* PyGithub
* GitHub Access Token

## Setup
* Create a free [Google Cloud Account](cloud.google.com/free/).
* Follow steps on [Installing Google Cloud SDK](https://cloud.google.com/sdk/install) to Install and Setup Google Cloud SDK
* Follow steps on [Python3](https://www.python.org/downloads/) to Install Python3
* Once you have the above setup ready, once review the [Building a Python App on App Engine](https://cloud.google.com/appengine/docs/standard/python3/building-app), to check if all the setup has been done correctly. 
* Clone this Repository to your system. 
* Create a GitHub access token with appropriate Access to invoke GitHub APIs and follow the steps mentioned on the GitHub Documentation: [Creating a personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
* Once you have the Access token created, we cannot save it in our Code as plain text, and thus we will leverage Google Cloud's Datastore storage and you can learn about how create an entity there by following steps in [Accessing your datastore content](https://cloud.google.com/datastore/docs/concepts/entities)
* Create Organization level Webhook under Organization Level Settings, and you could follow the steps outlined in the GitHub documentation [Creating Webhooks](https://developer.github.com/webhooks/creating/). Remember to use the same endpoint as your Webservice url created under your Google App Engine. 

## Usage
