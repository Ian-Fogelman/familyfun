import gspread
from google.oauth2.service_account import Credentials
import os 
import pandas as pd 
import requests
import json 
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv(override=True)

def return_gsheet_dataframe(SPREADSHEET_ID):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    SERVICE_ACCOUNT_FILE = os.path.join(parent_dir, "gdrive-427423-a3c987c18e0f.json")
    SPREADSHEET_ID = "1-CfzJXHOMWDgtRjOv8W0-fOiAgTCsrDFE7IYSHFpWnc"
    WORKSHEET_NAME = "Sheet1"  # ← Change if needed (or use index: 0 for first sheet)
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]     
    # "https://www.googleapis.com/auth/drive"  # ← Uncomment if using client.open("Title")
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES) 
    client = gspread.authorize(credentials) # Authorize the client
    spreadsheet = client.open_by_key(SPREADSHEET_ID) # Open the spreadsheet by ID (most reliable)
    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)  # Select the worksheet by name
    all_values = worksheet.get_all_values()
    if all_values:
        df = pd.DataFrame(all_values[1:], columns=all_values[0])
    else:
        df = pd.DataFrame()  # Empty dataframe if no data
    print("\nDataFrame created:")    # Show the resulting DataFrame
    print(df.shape)
    return df

def return_gist(url):
    r = requests.get(url)
    j = json.loads(r.text)
    return j

def write_reponse_to_json(json_text):
    # Write the raw JSON string to file
    output_file = "generated_questions.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")

def generate_new_questions():
    pass 

def open_pr_with_new_questions():
    pass 

def update_url_in_python_anywhere():
    pass

#email address to share with: python-reader@gdrive-427423.iam.gserviceaccount.com
SPREADSHEET_ID = "1-CfzJXHOMWDgtRjOv8W0-fOiAgTCsrDFE7IYSHFpWnc"
df = return_gsheet_dataframe(SPREADSHEET_ID)
LATEST_GIST_URL = "https://gist.githubusercontent.com/Ian-Fogelman/25e35e2e3d74aeca62ce2b1f3ef53c25/raw/782a8ef6ff60394e7892c696a3edf8d985530a9e/family_fun_data.json"
j = return_gist(LATEST_GIST_URL)
json_string = json.dumps(j, indent=2)  # indent=2 makes it very readable
#print('Total question count: ' + str(len(j['questions'])))
#print(j['questions'][0])
api_key = os.environ.get("gemeni_api_key")
client = genai.Client(api_key=api_key)  # auto-picks GEMINI_API_KEY or GOOGLE_API_KEY env var
df_string = df.to_markdown(index=False)

prompt = f"""You are a fun question generator for toddlers aged 3-6.
Use the following recent records (JSON format) and the dataframe below to create 5 interesting, simple, and age-appropriate questions.

Most recent data (JSON):
{json_string}

Current dataframe (markdown table):
{df_string}

Rules:
- Questions must be based on the most recent record(s) using the date column
- Keep them playful, curious, and easy for 3-6 year olds
- Return values must be in the format of the most recent data json format, i.e. in json and include the previous questions in the returned json!
- Make sure the return values dont have \u2019 characters when copied
- Make the json 1 line per age and q to save space i.e. 'age':'toddler', 'q': '123' """

# Then call as usual
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type":"application/json",
        "max_output_tokens": 8192,
        "temperature": 0.3
    }
)

print(response.text)
if response.candidates and response.candidates[0].finish_reason == "MAX_TOKENS":
    print("Hit token limit – response may be truncated or empty. Try increasing max_output_tokens.")

write_reponse_to_json(response.text)

