import pathlib
import textwrap
import time
import google.generativeai as genai
from google.api_core import exceptions
from IPython.display import display
from IPython.display import Markdown
from dotenv import load_dotenv
import os

load_dotenv()

my_api_key_google = os.getenv("MY_API_KEY_GOOGLE_API")

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
genai.configure(api_key=my_api_key_google)

model = genai.GenerativeModel('gemini-1.5-flash')

def remove_stars(text):
  """Removes all occurrences of '*' (single asterisk) and '**' (double asterisks) from the text."""
  return text.replace("*", "").replace("**", "").replace("##", "")

def promptResponse(prompt, retries=3):
  for attempt in range(retries):
    try:
      response = model.generate_content(prompt)
      text = response.text
      text_without_stars = remove_stars(text)
      return text_without_stars
    except exceptions.InternalServerError:
      if attempt < retries - 1:
        # Log the error and wait before retrying
        print(f"InternalServerError occurred. Retrying in {attempt+1} attempt(s).")
        time.sleep(2**attempt)  # Exponential backoff
      else:
        print(f"Failed to generate response after {retries} attempts.")
        # Handle the final failure (e.g., return a default message)
        return "An unexpected error occurred at server side. Please try again later."