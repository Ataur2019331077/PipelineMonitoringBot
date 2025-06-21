from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

def gemini_response(text):
    try:
        prompt = f"""
        You are a helpful assistant. You will be given newsheadline and link and you should add
        another filed named category and in category should be kept category of the headline and return as it 's
        previous format. Here is the newsheadlines with link {text}.
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()

        generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
        generated_text = generated_text.replace("```json", "").replace("```", "").strip()
    
        return generated_text
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def make_decision(text):
    try:
        prompt = f"""
        You are a helpful assistant of manager. You will be given a message from pipeline and 
        you need to tell manager if if he needs to mail someone or not according to the message.
        Here is the message {text}.
        Your response should also include the message Here is the sample output in json format:
        {{
            "message": "The daily sun news added. \n\n",
            "decision_message": "Hi Sir, I am looking that the prothom alo news is not added. Please check it out. Do you want to make a draft of
            the mail to corresponding person?",
        }}
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()

        generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
        generated_text = generated_text.replace("```json", "").replace("```", "").strip()
    
        return generated_text
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def gemini_query(query, last_context):
    try:
        prompt = f"""
        You are a helpful assistant. You will be given a message from user and you need to answer the question according to the last context.
        Here is the last context {last_context} and here is the user query: {query}.
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()

        generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
        generated_text = generated_text.replace("```json", "").replace("```", "").strip()
    
        return generated_text
    
    except Exception as e:
        print(f"Error: {e}")
        return None