from urllib.parse import urlencode

import requests
from flask import Flask, request
from flask_cors import CORS

from .Utils import load_json

app = Flask(__name__)
CORS(app)
title = ""
next_op = None


@app.route("/")
def operation():
    config = load_json("Config.json")
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    code = request.args.get("code")
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8080/",
    }

    resp = requests.post("https://id.twitch.tv/oauth2/token", data=data).json()
    token = resp["access_token"]

    headers = {
        "Client-Id": client_id,
        "Authorization": "Bearer " + token,
    }

    # get broadcaster id
    data = {"login": [config["broadcaster_id"]]}

    url = "https://api.twitch.tv/helix/users?" + urlencode(data, doseq=True)
    resp = requests.get(url, headers=headers).json()
    broadcaster_id = resp["data"][0]["id"]

    print(f"Next Operation: {next_op}")

    if next_op == "title":
        data = {"broadcaster_id": broadcaster_id, "title": title}

        url = "https://api.twitch.tv/helix/channels?" + urlencode(data, doseq=True)
        resp = requests.patch(url, headers=headers)

    elif next_op == "ads":
        data = {"broadcaster_id": broadcaster_id, "length": 30}

        url = "https://api.twitch.tv/helix/channels/commercial"
        resp = requests.post(url, headers=headers, json=data)

    return resp.content, resp.status_code


@app.route("/title")
def title():
    global title, next_op
    title = request.args.get("title")
    next_op = "title"

    return "", 204


@app.route("/ads")
def ads():
    global next_op
    next_op = "ads"

    return "", 204


def main():
    app.run(port=8080)


if __name__ == "__main__":
    main()
