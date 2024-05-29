import requests

def send_discord_message(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.json())

def send_discord_image(webhook_url, file_path):
    with open(file_path, 'rb') as f:
        payload = {
            'file': (file_path, f, 'image/png')
        }
        response = requests.post(webhook_url, files=payload)
        if response.status_code == 204:
            print("Image sent successfully")
        else:
            print(f"Failed to send image: {response.status_code}")
            print(response.json())
