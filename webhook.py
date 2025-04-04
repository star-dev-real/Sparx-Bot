import requests
import json
from datetime import datetime
from urllib.parse import urlparse

class WebhookSender:
    @staticmethod
    def send(url, data):
        try:
            if not url.startswith(('http://', 'https://')):
                return False
                
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                url,
                data=json.dumps(data),
                headers=headers,
                timeout=5
            )
            return response.ok
            
        except Exception as e:
            print(f"Webhook error: {e}")
            return False

    @staticmethod
    def send_discord(url, content, username=None, embeds=None):
        """Discord-specific webhook"""
        data = {
            "content": content,
            "username": username or "Star-EXE Bot",
            "embeds": embeds or []
        }
        return WebhookSender.send(url, data)