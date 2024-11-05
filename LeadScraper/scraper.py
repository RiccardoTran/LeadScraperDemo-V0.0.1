import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY_GROQ')

driver = webdriver.Chrome()

url = 'https://www.eurocominnovazione.it/'  # Inserisci qui il tuo URL

driver.get(url)

content = driver.find_element(By.TAG_NAME, 'body').text

driver.quit()

api_url = 'https://api.groq.com/openai/v1/chat/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

prompt = f"""Write in italian. Create a personalized message for an IT consulting business developer, pitching a service to create automated list of prospets to the General Manager, gathering information on the client from the scraped site content:
{content}"""

data = {
    "model": "llama-3.1-70b-versatile",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}

response = requests.post(api_url, headers=headers, data=json.dumps(data))
message_content = response.json()['choices'][0]['message']['content'] 
print(message_content)
