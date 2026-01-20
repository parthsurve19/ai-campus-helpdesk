import google.generativeai as genai
import os
import json

# --- CONFIGURATION ---
# Ideally, store this in a .env file, but for now, paste your key here.
GOOGLE_API_KEY = "AIzaSyDzPiTVj_rf_S9GLYQmXuXOfWpuJFwjrQY"

genai.configure(api_key=GOOGLE_API_KEY)

def grade_submission_with_gemini(file_path, rubric_text):
    """
    Uploads a file to Gemini, asks it to grade based on the rubric,
    and returns a dictionary with 'marks' and 'feedback'.
    """
    try:
        # 1. Upload the file to Gemini
        # Gemini 1.5 Pro can read PDFs and Images directly via the File API
        print(f"Uploading file: {file_path}...")
        sample_file = genai.upload_file(path=file_path, display_name="Student Submission")
        
        # 2. Create the Prompt
        # We enforce JSON output so your frontend teammate can easily display it.
        prompt = f"""
        You are a strict university professor. 
        Your task is to grade the attached student assignment based ONLY on the following grading rubric:
        
        RUBRIC:
        {rubric_text}
        
        Please analyze the file and provide:
        1. Marks Obtained (out of 100).
        2. Detailed Feedback (Strengths and Areas for Improvement).
        
        Output your response strictly in this JSON format:
        {{
            "marks": "85/100",
            "feedback": "Your explanation of the concept was clear, but you missed..."
        }}
        """

        # 3. Call the Model
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        response = model.generate_content([sample_file, prompt])

        # 4. Clean up (Optional: Parsing the JSON)
        # Sometimes AI adds ```json at the start, we remove it to be safe
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result_json = json.loads(clean_text)
        
        return result_json

    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "marks": "0/100", 
            "feedback": "Error: Could not process the file. Please try again."
        }