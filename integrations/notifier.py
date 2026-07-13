import os
import requests

class Notifier:
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send_message(self, message: str):
        if not self.webhook_url:
            return "No webhook configured. Message logged locally."

        payload = {"text": f"KANO Update: {message}"}
        try:
            requests.post(self.webhook_url, json=payload)
            return "Notification sent."
        except Exception as e:
            return f"Notification error: {e}"

    def request_approval(self, task_name: str, details: str):
        msg = f"⚠️ APPROVAL REQUIRED: {task_name}\nDetails: {details}\nRespond via CLI."
        return self.send_message(msg)
