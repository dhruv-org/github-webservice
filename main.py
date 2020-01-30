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
#from hmac import HMAC, compare_digest
#from hashlib import sha1
#import hmac



from flask import Flask, render_template

import logging
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)

gh = Github("5e7b1d6424b422b7a4cedc433437717506640382")

'''
def verify_signature(data):
    #payload = pickle.dumps(request.DATA)
    received_sign = request.headers.get('X-Hub-Signature').split('sha1=')[-1].strip()
    print(received_sign)
    secret="ptmihemlzj33437717506640382".encode()
    #signature = hmac.new(APP_KEY, request, hashlib.sha1).hexdigest()
    #expected_sign = HMAC(key=secret, msg=data, digestmod=sha1).hexdigest()
    expected_sign = 'sha1=' + hmac.new(secret, data, sha1).hexdigest()
    #signature = hmac.new(APP_KEY, payload, hashlib.sha1).hexdigest()
    if compare_digest(received_sign, expected_sign):
        return True
    else:
        return False
'''

@app.route('/')
def root():
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
    if request.method == 'POST':
        data = request.get_json()
        #valid=verify_signature(data)
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
            branch = gh.get_repo(repo_full_name).get_branch("master")
            membership = user.get_organization_membership(org)
            branch_users = branch.get_user_push_restrictions()
            push_restriction_active = False
            try:
                logging.info(branch_users[0])
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

            logging.info(output)

        return render_template('github_webhook.html',data=output)

    return render_template('github_webhook.html',"GET Request")

"""
    logging.info("Text info")
    logging.debug("Text debug")
    logging.warning("Text warning")
    logging.error("Text error")
    logging.critical("Text critical")
"""
    

@app.route('/dhruv_index.html')
def dhruv_root():
    return render_template('dhruv_index.html')

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
