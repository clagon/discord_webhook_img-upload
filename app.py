import json
import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def isValidExtention(filename: str) -> bool:
    if isinstance(filename, str):
        extention_allowed = ["png", "jpeg", "jpg", "gif", "webp"]
        extention = filename.split(".")[1]
        return extention in extention_allowed
    return False


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file_uploaded = request.files["file"]
        filename = file_uploaded.filename
        content = request.form.get("content")
        data = {
            "username": "testing",
            "content": content,
            # "avatar_url": ,""
        }
        r = None
        if filename and isValidExtention(filename):
            body = {
                "payload_json": json.dumps(data)
            }
            files = {
                "attachment": (filename, file_uploaded.read())
            }
            r = requests.post(
                WEBHOOK_URL,
                body,
                files=files
            )
        else:
            headers = {
                "content-type": "application/json"
            }
            r = requests.post(
                WEBHOOK_URL,
                json=data,
                headers=headers
            )
        return r.content
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
