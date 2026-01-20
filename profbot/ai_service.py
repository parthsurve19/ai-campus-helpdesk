import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This helps Python find the .env file even if it's hiding.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Get the key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# DEBUG CHECK
if not GOOGLE_API_KEY:
    print("❌ ERROR: Still cannot find the API Key in .env file!")
else:
    print("✅ SUCCESS: API Key found!")

genai.configure(api_key=GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)

def grade_submission_with_gemini(file_path, rubric_text):
    print(f"--- Processing File: {file_path} ---")
    try:
        # 3. Upload File
        sample_file = genai.upload_file(path=file_path, display_name="Student Submission")
        print("File uploaded successfully.")

        # 4. Prompt
        prompt = f"""
        You are a strict professor. Grade this assignment based on the rubric:
        {rubric_text}

        Return a VALID JSON object exactly like this:
        {{
            "marks": "85/100",
            "feedback": "Short summary of feedback here."
        }}
        Do not add any markdown formatting or extra text.
        """

        # 5. Call Model
        model = genai.GenerativeModel("gemini-1.5-flash") 
        response = model.generate_content([sample_file, prompt])
        
        # DEBUG: Print exactly what Gemini said
        print(f"RAW AI RESPONSE: {response.text}")

        # 6. Clean and Parse JSON
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        
        if json_match:
            clean_json = json_match.group(0)
            result = json.loads(clean_json)
            return result
        else:
            return {"marks": "0/100", "feedback": "AI returned invalid format. Check terminal for details."}

    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "marks": "0/100", 
            "feedback": f"Error: {str(e)}"
        }