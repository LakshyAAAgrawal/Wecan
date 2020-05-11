import requests

SLACK_WEBHOOK = "https://hooks.slack.com/services/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"

def send_slack_message(txt):
    data = {
        "Content-type": "application/json",
        "text": txt
    }
    requests.post(url = SLACK_WEBHOOK, json = data)
