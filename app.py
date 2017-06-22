from subprocess import Popen, PIPE
from json import dumps
from requests import get
from hashlib import md5

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return "Hello World!"


@app.route("/safety", methods=["POST"])
def safety():
    # set env
    msg = {}
    url = request.form['url']
    if not url.startswith("http"):
        msg['status'] = False
        msg['data'] = "No Hack"
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

        m = md5()
        m.update(url)
        url_hash = m.hexdigest()

        file_name = "cache/{}.html".format(url_hash)

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

