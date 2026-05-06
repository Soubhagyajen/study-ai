import os
import json
import urllib.request
from urllib.error import URLError, HTTPError

def generate_study_plan(user_data):
    """
    Connects to Google Gemini API to generate a structured strict JSON study plan.
    Input: user_data dict containing subjects, upcoming exams, study progress.
    Output: dict with 'tasks' and 'quote'.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Fallback default plan if API key is not yet set
    if not api_key:
        print("[WARNING] GEMINI_API_KEY environment variable not set. Falling back to default plan.")
        return {
            "tasks": [
                {"subject": "Vedic Mathematics", "duration": 45, "priority": "High", "category": "Quantitative"},
                {"subject": "Sanskrit Syntax", "duration": 30, "priority": "Medium", "category": "Grammar"}
            ],
            "quote": "Discipline is the bridge between goals and success."
        }

    prompt = f"""
Create a highly personalized daily study plan for a student based on these details:
Subjects: {user_data.get('subjects', [])}
Upcoming Exams: {user_data.get('upcoming_exams', [])}
Progress Overview: {user_data.get('progress', [])}

You must return ONLY a strictly valid JSON object without any markdown formatting or comments. 
The JSON must follow exactly this schema:
{{
    "tasks": [
        {{
            "task": "Specific topic to study",
            "subject": "Name of Subject",
            "duration": 60,
            "category": "e.g., Theory, Practice, Revision",
            "estimated_minutes": 60,
            "priority": "High"
        }}
    ],
    "quote": "A powerful motivational quote about discipline and learning, preferably slightly ancient/stoic sounding."
}}
Ensure the response is raw JSON only.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts":[{"text": prompt}]}]
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Navigate standard Gemini response payload
            text_response = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            
            # Clean possible markdown wrapping if Gemini ignores instructions
            text_response = text_response.strip()
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            if text_response.startswith("```"):
                text_response = text_response[3:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
                
            return json.loads(text_response.strip())

    except (URLError, HTTPError) as e:
        print(f"Gemini API Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Gemini JSON Parsing Error. Response was not properly formatted JSON: {e}")

    # Ultimate fallback string representation if API fails out
    return {
        "tasks": [
            {"task": "Analyze API Error", "subject": "System", "estimated_minutes": 15, "priority": "High", "category": "Debugging"}
        ],
        "quote": "The API stumbled, but the Shishya pushes forward."
    }
