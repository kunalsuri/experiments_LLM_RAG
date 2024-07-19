# About: Simple code to execute the question, i.e., the prompt, on the Ollama Server

import requests
import json

url = 'http://localhost:11434/api/generate'
data = {
    "model": "llama2",
    "prompt": "What is the capital of France?"
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)
full_response = []

try:
    count = 0
    for line in response.iter_lines():
        if line:
            decoded_line = json.loads(line.decode('utf-8'))
            
            full_response.append(decoded_line['response'])
finally:
    response.close()
print(''.join(full_response))
