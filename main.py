# https://dhruv-webservices.appspot.com/
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
import datetime
from github import Github
from modules.fibs import *
import logging
from flask import request
import json
from google.cloud import datastore

from flask import Flask, render_template

import logging
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)

datastore_client = datastore.Client()

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times



query = datastore_client.query(kind='github')
data = list(query.fetch())
git_accesskey = data[0]['secretkey']
git_webhook_secret = data[1]['secretkey']
gh = Github(git_accesskey)

def debug_keys():
    debug = request.args.get('debug')
    if debug == "true":
        logging.info("git_accesskey:"+git_accesskey)
        logging.info("git_webhook_secret:"+git_webhook_secret)


@app.route('/')
def root():
    debug_keys()
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    #modules.fibs.fib(1000)
    data=fib2(1000)
    print(data)

    
    repo = gh.get_user().get_repos()

    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times,datas=repo[0])

@app.route('/ghwebhook', methods=['GET', 'POST'])
def github_webhook():
    debug_keys()
    if request.method == 'POST':
        data = request.get_json()
        logging.info("*************Text debug-Json-dump***********")
        logging.info(json.dumps(data))
        logging.info("*************Text debug-Json-dump***********")
        logging.info(('action' in data and 'pull_request' in data) and (data['action'] == "opened"))
        output = False

        if ('before' in data and 'created' in data) and (data['before'] == "0000000000000000000000000000000000000000" and data['created'] == True):
            repo_full_name = data['repository']['full_name']
            creator_name = data['sender']['login'] 
            logging.info("*************Text debug-Create-Branch-Restriction***********")
            output = "Repo-Created-URL: " + repo_full_name + " ; Owner: " + creator_name
            logging.info(output)
            branch = gh.get_repo(repo_full_name).get_branch("master")
            branch.edit_protection(user_push_restrictions=[creator_name])
            logging.info("*************Text debug-Create-Branch-Restriction***********")

        if ('action' in data and 'pull_request' in data) and (data['action'] == "opened"):
            repo_full_name = data['repository']['full_name']
            creator_name = data['sender']['login'] 
            #creator_name = "dhruv-gupta-live"
            #creator_name = "dhruv-instart"
            org = data['organization']['login']
            user = gh.get_user(creator_name)
            repo = gh.get_repo(repo_full_name)
            branch = repo.get_branch("master")
            membership = user.get_organization_membership(org)
            branch_users = branch.get_user_push_restrictions()
            push_restriction_active = False
            repo_owner = False
            org_owner = 'dhruvg20'
            try:
                repo_owner = branch_users[0].login
                push_restriction_active = True
            except Exception as err:
                logging.info("push_restriction_active: " + str(push_restriction_active))

            user_access = False
            org_admin = False

            logging.info("*************Text debug-PullRequest-IssueCreation***********")
            output = "PullRequest-Created: " + repo_full_name + " ; Owner: " + creator_name
            logging.info(output)
            logging.info("*************Text debug-PullRequest-IssueCreation***********")

            if membership.state == 'active' and membership.role != 'admin':
                output = creator_name + " : OrgMembership: Not Admin"
                logging.info(output)
                if push_restriction_active == True:
                    for buser in branch_users:
                        logging.info(buser)
                        if buser.login == creator_name:
                            user_access = True
                            break
                    logging.info(creator_name + " Repo Access : " + str(user_access))
                
            elif membership.state == 'active' and membership.role == 'admin':
                output = creator_name + " : OrgMembership: Admin"
                org_admin = True
            

            if org_admin == False:
                if user_access == True:
                    output = creator_name + " : OrgMembership: Not Admin: RepoAccess: Granted"
                elif user_access == False:
                    output = creator_name + " : OrgMembership: Not Admin: RepoAccess: Not Granted: Create Issue"
                    #label = repo.get_label("My Label")
                    #repo.create_issue(title="This is a new issue", labels=[label], body="This is the issue body @dhruvg20")
                    title = "Branch Restriction - repo:" + repo_full_name + " - member:" + creator_name
                    if repo_owner == False:
                        body = '''
Attention: @{org_owner}, @{creator_name}
Repository: {repo_full_name}
There is branch restriction setup, such that only the creator or adminstrator has push permission.
                        '''.format(org_owner=org_owner,creator_name=creator_name,repo_full_name=repo_full_name)
                    elif repo_owner == org_owner:
                        body = '''
Attention: @{repo_owner}, @{creator_name}
Repository: {repo_full_name}
There is branch restriction setup, such that only the creator or adminstrator has push permission.
                        '''.format(repo_owner=repo_owner,creator_name=creator_name,repo_full_name=repo_full_name)
                    else:
                        body = '''
Attention: @{repo_owner}, @{org_owner}, @{creator_name}
Repository: {repo_full_name}
There is branch restriction setup, such that only the creator or adminstrator has push permission.
                        '''.format(repo_owner=repo_owner,org_owner=org_owner,creator_name=creator_name,repo_full_name=repo_full_name)
                    repo.create_issue(title=title, body=body)                    
            logging.info(output)
            logging.info("Issue-Title:"+title)
            logging.info("Issue-Body:"+body)

        return render_template('github_webhook.html',data=output)

    return render_template('github_webhook.html',data="GET Request")
    
@app.route('/dhruv_index.html')
def dhruv_root():
    debug_keys()
    return render_template('dhruv_index.html')

@app.route('/accesslist.html')
def accesslist():
    debug_keys()
    # Store the current access time in Datastore.
    store_time(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    times = fetch_times(10)

    return render_template(
        'accesslist.html', times=times)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
