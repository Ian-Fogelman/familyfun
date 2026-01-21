from flask import Flask, render_template, request
import json
import random
import os 

app = Flask(__name__)

# Global questions list
QUESTIONS = []

def load_questions():
    global QUESTIONS
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "generated_questions.json")
    
    QUESTIONS = []
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, dict) and "questions" in data:
            QUESTIONS = data["questions"]
        elif isinstance(data, list):
            QUESTIONS = data
        else:
            print(f"Unexpected data structure: {type(data)}")
            return
            
        print(f"Loaded {len(QUESTIONS)} questions successfully from {file_path}")
        
        # Debug: Print all unique age values found
        age_values = set()
        for q in QUESTIONS:
            if isinstance(q, dict) and "age" in q:
                age_values.add(f"'{q['age']}'")
        print(f"Unique age values in JSON: {sorted(age_values)}")
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error in {file_path}: {e}")
    except Exception as e:
        print(f"Failed to load questions from {file_path}: {e}")

load_questions()

@app.route("/")
def index():
    raw_age = request.args.get("age", "all")
    requested_age = (raw_age or "all").lower().strip()
    
    print(f"Raw input: '{raw_age}' → Normalized: '{requested_age}'")
    
    if requested_age in ["", "all"]:
        available = QUESTIONS
    else:
        # Very forgiving matching with type checking
        available = [
            q for q in QUESTIONS
            if isinstance(q, dict) and isinstance(q.get("age"), str) and q.get("age", "").lower().strip() == requested_age
        ]
    
    print(f"Found {len(available)} matching questions for '{requested_age}'")
    
    # Debug: if no matches, show what we're comparing
    if not available and requested_age not in ["", "all"]:
        sample_ages = [q.get("age") for q in QUESTIONS[:5] if isinstance(q, dict)]
        print(f"Sample ages from JSON: {sample_ages}")
    
    if available:
        selected = random.choice(available)
        question_text = selected.get("q", "No question available")
        age_group = selected.get("age", "Unknown").title()
    else:
        # Safe extraction of available age groups
        available_ages = set()
        for q in QUESTIONS:
            if isinstance(q, dict) and isinstance(q.get("age"), str):
                available_ages.add(q.get("age", "").title())
        
        question_text = (
            "Oops! No questions found for this age group... 😅<br>"
            f"Available groups: {', '.join(sorted(available_ages)) if available_ages else 'None found'}"
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
