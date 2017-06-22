from subprocess import Popen, PIPE
from os.path import exists
from json import dumps
from requests import get
from hashlib import md5

from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)


def get_md5(url):
    m = md5()
    m.update(url)
    url_hash = m.hexdigest()
    return url_hash


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/main")
def main_():
    return render_template("main.html")


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route("/safety", methods=["POST"])
def safety():
    # set env
    msg = {}
    url = request.form['url']
    if not url.startswith("http"):
        msg['status'] = False
        msg['data'] = "No Hack"
        return dumps(msg)

    url_hash = get_md5(url)

    file_name = "cache/{}.html".format(url_hash)

    if exists(file_name):
        msg['status'] = True
        return dumps(msg)

    p = Popen(["phantomjs", "run.js", url], stdout=PIPE)
    data, err = p.communicate()

    msg['status'] = True

    return dumps(msg)


@app.route('/browse', methods=['POST'])
def browse():
    msg = {}

    url = request.form['url']

    try:
        data = get(url).content

        url_hash = get_md5(url)

        file_name = "cache/{}.html".format(url_hash)

        if exists(file_name):
            with open(file_name, 'rb') as f:
                data = f.read()
                f.close()

            msg['status'] = True
            msg['data'] = data
            msg['cache'] = file_name
        
            return dumps(msg)

        with open(file_name, 'wb') as f:
            f.write(data)
            f.close()

        msg['status'] = True
        msg['data'] = data
        msg['cache'] = file_name

    except Exception as e:
        msg['status'] = False
        msg['data'] = e

    return dumps(msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

