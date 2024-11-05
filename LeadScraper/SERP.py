import csv
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY_SERP')

url = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
payload = '[{"keyword":"site:linkedin.com/company telecomunicazioni linkedin italia  -\\"offerte di lavoro\\" ","location_code":2380,"language_code":"it","device":"desktop","os":"windows","depth":100}]'
headers = {
    'Authorization': f'Basic {api_key}',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

response_json = response.json()

print(response_json)

if 'tasks' in response_json and response_json['tasks']:
    if 'result' in response_json['tasks'][0] and response_json['tasks'][0]['result']:
        csv_columns = ['url', 'title', 'description', 'rank_absolute']

        csv_data = []
        for item in response_json['tasks'][0]['result'][0]['items']:
            csv_data.append({
                'url': item['url'],
                'title': item['title'],
                'description': item.get('description', ''),  # Use .get() to avoid KeyError
                'rank_absolute': item['rank_absolute']
            })

        csv_file = "response.csv"
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                writer.writerows(csv_data)
            print(f"Data successfully written to {csv_file}")
            print(f"CSV file path: {csv_file}")
        except IOError:
            print("I/O error")
    else:
        print("Error: 'result' key not found in the first task.")
else:
    print("Error: 'tasks' key not found in the response.")
