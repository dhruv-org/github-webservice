# A GitHub Organization Events listens Web Service

This is a example setup for running a Web Service on Google App Engine, which gets invoked from GitHub Webhooks to maintains branches to be automatically protected upon creation and issue registered. 

## Requirements
* Google Cloud SDK Account
    * App Engine
    * Datastore
* Python3
* Flask
* [PyGithub](https://pygithub.readthedocs.io/en/latest/introduction.html)
* GitHub Access Token

## Setup
1. Create a free [Google Cloud Account](cloud.google.com/free/).
2. Follow steps on [Installing Google Cloud SDK](https://cloud.google.com/sdk/install) to Install and Setup Google Cloud SDK
3. Follow steps on [Python3](https://www.python.org/downloads/) to Install Python3
4. Once you have the above setup ready, once review the [Building a Python App on App Engine](https://cloud.google.com/appengine/docs/standard/python3/building-app), to check if all the setup has been done correctly. 
5. Clone this Repository to your system. 
6. Create a GitHub access token with appropriate Access to invoke GitHub APIs and follow the steps mentioned on the GitHub Documentation: [Creating a personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
7. Once you have the Access token created, we cannot save it in our Code as plain text, and thus we will leverage Google Cloud's Datastore storage and you can learn about how create an entity there by following steps in [Accessing your datastore content](https://cloud.google.com/datastore/docs/concepts/entities)
9. Once you have the GitHub Repository cloned on your System. 
10. Make sure you have setup the GitHub Access Token(Setup Step 6) and saving it on the Google Cloud Datastore(Setup Step 7).
11. Once you have the above step setup correcly, run testing on your local system by running the following:
```python3 main.py```
This will run a webservice at [http://127.0.0.1:8080/](http://127.0.0.1:8080/) and you could check if everything is working correctly on the console's logging. 
On the above link access you will see some testing templates to verify everything is working correctly. 
12. Once local system testing looks correct, then you can deploy the Google App Engine application on Google Cloud, by running the command:
```gcloud app deploy```
13. Once the above command runs Successfully, you would see the Google App Engine endpoints like https://[accountname].appspot.com
14. Create Organization level Webhook under Organization Level Settings, and you could follow the steps outlined in the GitHub documentation [Creating Webhooks](https://developer.github.com/webhooks/creating/). Remember to use the same endpoint as your Webservice url created under your Google App Engine. The Webhook endpoint/url needs to be https://[accountname].appspot.com/ghwebhook, where all the events of your Organization will be sent as POST request from GitHub to Google App Engine.

## Usage
I will share the example of the Organization owned and created by me: dhruv-org.
It has 3 Members with the following Access:
1. dhruv-gupta-live - Member
2. dhruv-instart - Member
3. dhruvg20 - admin

Following Branch Protection or Issue creation rules are setup on the Organization: 
* If any member creates a Repository, then he gets a Branch Restriction created under him, such that only he or the admin can make a change to the master branch. 
* If a member who has not created the Repository or is not a Admin on the Organization, then a Issue will be opened mentioning Admin, Branch Creator and Pull request creater called out, stating the restriction. 

## Example Usage: 

## Troubleshooting:

## Github Python Usage:

* Test
