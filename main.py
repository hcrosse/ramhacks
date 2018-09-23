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
from flask import Flask, render_template, request
from flask_sslify import SSLify
import genius
import recommend

app = Flask(__name__)
sslify = SSLify(app, permanent=True)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        lyrics = genius.get_lyrics(request.args['query'])
    else:
        lyrics = genius.get_lyrics(request.form['query'])
    data = recommend.recommend(lyrics)
    return render_template('similar.html', data=data)


@app.route('/lyrics', methods=['GET'])
def display_lyrics():
    title = request.args['title'].title()
    artist = request.args['artist'].title()
    lyrics = genius.get_lyrics(title, artist).split('\n')
    data = {'title': title, 'artist': artist, 'lyrics': lyrics}
    return render_template('lyrics.html', data=data)


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
