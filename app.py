from flask import Flask, render_template, request
import requests
import json
import random

app = Flask(__name__)

# Global questions list
QUESTIONS = []

def load_questions():
    global QUESTIONS
    url = 'https://gist.githubusercontent.com/Ian-Fogelman/25e35e2e3d74aeca62ce2b1f3ef53c25/raw/89c68a1d19f9a23b21011555b8786b1bccd73bae/family_fun_data.json'
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        QUESTIONS = data.get("questions", [])
        print(f"Loaded {len(QUESTIONS)} questions successfully")
    except Exception as e:
        print(f"Failed to load questions: {e}")
        QUESTIONS = []

load_questions()

@app.route("/")
def index():
    raw_age = request.args.get("age", "all")
    requested_age = (raw_age or "all").lower().strip()  # handles None, empty string, spaces

    print(f"Raw input: '{raw_age}' → Normalized: '{requested_age}'")  # better debug

    if requested_age in ["", "all"]:
        available = QUESTIONS
    else:
        # Very forgiving matching
        available = [
            q for q in QUESTIONS
            if q.get("age", "").lower().strip() == requested_age
        ]

    print(f"Found {len(available)} matching questions for '{requested_age}'")

    if available:
        selected = random.choice(available)
        question_text = selected["q"]
        age_group = selected["age"].title()  # → "Tween", "Young Adult", etc.
    else:
        question_text = (
            "Oops! No questions found for this age group... 😅<br>"
            f"Available groups: {', '.join(sorted(set(q['age'].title() for q in QUESTIONS)))}"
        )
        age_group = requested_age.title() if requested_age not in ["", "all"] else "Any Age"

    return render_template(
        "index.html",
        q=question_text,
        a=age_group,
        requested_age=requested_age,
    )

if __name__ == "__main__":
    app.run(debug=True)
