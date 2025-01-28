import requests
import json

class LMService():
    def __init__(self):
        self.lm_url = "http://localhost:11434/api/chat"
        self.headers = {'Content-Type': 'application/json'}
        self.model = "hf.co/bartowski/granite-3.1-2b-instruct-GGUF:Q6_K"
        
    def lm_response(self, prompt):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Act as a friendly and concise conversational assistant. Answer questions clearly, stay conversational, and keep responses short unless more detail is requested."},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(self.lm_url, json=payload, headers=self.headers, stream=True)
            
            if response.status_code == 200:
                response_parts = response.text.split('\n')
                content = ""
                for part in response_parts:
                    part = part.strip()
                    if not part:
                        continue
                    try:
                        response_dict = json.loads(part)
                        message = response_dict.get('message', {})
                        content += message.get('content', '')
                    except json.JSONDecodeError as e:
                        return "I'm sorry I cannot help with that."
                return content.strip()
            else:
                return "I'm Sorry I cannot help with that."
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass
        
        return "I'm sorry I cannot help with that."