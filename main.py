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

# [START gae_python38_render_template]
import datetime
import pytz

from flask import Flask, render_template
from flask import send_from_directory
from flask_bootstrap import Bootstrap
from google.cloud import firestore

import os

from classes import ScheduleParser

datastore_client = firestore.Client()

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def root():
    doc = datastore_client.collection('Derby').document('Schedule')
    scheduleRes = doc.get().to_dict()
    doc = datastore_client.collection('Derby').document('Cars')
    carsRes = doc.get().to_dict()

    return render_template('public.html',
                           data=scheduleRes['data'],
                           columns=scheduleRes['columns'],
                           dataCars=carsRes['data'],
                           columnsCars=carsRes['columns'],
                           )

@app.route('/gallery')
def gallery():
    gallery = []
    basePath = 'static/gallery/'
    dirs = os.listdir(basePath)
    for d in dirs:
        if(os.path.isdir(basePath + d)):
            carNum = d
            carPath = 'gallery/' + carNum + '/'
            files = os.listdir('static/' + carPath)
            images = []
            youTubeId = ''
            for file in files:
                if '.id' in file:
                    f = open("static/" +carPath+file, "r")
                    youTubeId = f.readline()
                elif ('.jpg' in file or '.png' in file):
                    images.append(carPath + file)
            carInfo = {'carNum': carNum, 'images': images, 'youTubeId': youTubeId}
            gallery.append(carInfo)

    return render_template('gallery.html', gallery=gallery)

@app.route('/bbcode')
def bbcode():
    return render_template('bbcode.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':

    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_render_template]
