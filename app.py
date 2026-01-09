from flask import Flask, render_template
import requests
import json
app = Flask(__name__)

@app.route("/")
def index():
    r = requests.get('https://gist.githubusercontent.com/Ian-Fogelman/25e35e2e3d74aeca62ce2b1f3ef53c25/raw/e5da34946e287b4f806675890dc723ac34240f8c/family_fun_data.json')
    print(r.text)
    j = json.loads(r.text)
    first_question = j["questions"][0]

    # Renders the index.html file found in the 'templates' folder
    return render_template("index.html", name=first_question)