import re
import requests
from generativeAI import promptResponse
from dotenv import load_dotenv
import os

load_dotenv()

my_api_key_bot = os.getenv("MY_API_KEY_CHATBOT")


base_url = my_api_key_bot

def read_msg(offset):
    parameters = {
        "offset": offset
    }

    resp = requests.get(base_url + "/getUpdates", data=parameters)
    data = resp.json()

    for result in data["result"]:
        send_msg(result)

    if data["result"]:
        return data["result"][-1]["update_id"] + 1

def auto_answer(message):
    message = re.sub(r'[^a-zA-Z\s]', '', message).lower()  # Preprocess the message
    message = re.sub(r'\s+', ' ', message).strip().lower()

    # Check if the message text is empty
    if not message:
        return None

    # Example API call (replace with actual API calls)
    # response = requests.get(f"https://api.example.com/definitions/{message}")
    definition = promptResponse(message) # Extract definition from API response

    if definition:
        return definition
    else:
        # Example Google Search API call (replace with actual API calls)
        search_response = requests.get(f"https://www.google.com/search?q={message}")
        # Parse search results to extract relevant information (implementation details omitted)
        return "Sorry, I couldn't find a specific definition. Here's what I found on the web..."
        
def send_msg(message):
    chat_id = message["message"]["chat"]["id"]
    text = message["message"]["text"]
    message_id = message["message"]["message_id"]
    answer = auto_answer(text)

    parameters = {
        "chat_id": chat_id,
        "text": answer,
        "reply_to_message_id": message_id
    }

    resp = requests.get(base_url + "/sendMessage", data=parameters)

offset = 0

while True:
    offset = read_msg(offset)