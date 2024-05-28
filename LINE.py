import requests

def send_line_message(token, user_id, message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text":  message
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.json())

CHANNEL_ACCESS_TOKEN = "GltYV17+fvfRAnf/Rezy8Ph720WkAXP6JYQSf6OFAJCKImRn0KN0dMckb8kC5qLv0uxok4CMhxiqClBF3wdnyT3P4wzNwQRUCJ2AciE/pAylKz0WA+vopw+59qjAZw7bUtWsfxu9IJ8IrX9boS+XCAdB04t89/1O/w1cDnyilFU="
USER_ID = "Ub46f07acc1c828c5c1f8362b82181e45"
MESSAGE = "Hello, this is a test message from Python!"

send_line_message(CHANNEL_ACCESS_TOKEN, USER_ID, MESSAGE)
