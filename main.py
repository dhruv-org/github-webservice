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


from flask import Flask, render_template

import logging
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)


@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    #modules.fibs.fib(1000)
    data=fib2(1000)
    print(data)

    g = Github("5e7b1d6424b422b7a4cedc433437717506640382")
    repo = g.get_user().get_repos()

    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times,datas=repo[0])

@app.route('/ghwebhook', methods=['GET', 'POST'])
def github_webhook():
    if request.method == 'POST':
        data = request.get_json()
        logging.info("*************Text debug***********")
        logging.info(json.dumps(data))
        #logging.info("Text debug" + str(data))
        logging.info("*************Text debug***********")
        return render_template('dhruv_index.html')
    logging.info("Text info")
    logging.debug("Text debug")
    logging.warning("Text warning")
    logging.error("Text error")
    logging.critical("Text critical")
    return render_template('github_webhook.html')

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
