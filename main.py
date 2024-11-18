from fastapi import FastAPI, Request, Form, Depends, BackgroundTasks
from twilio.rest import Client
from dotenv import load_dotenv
import os

app = FastAPI()

ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')


def send_message(destination_number: str, message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        from_=TWILIO_PHONE_NUMBER,
        to=destination_number,
        body=message,
    )

    return message.sid


async def get_request_form(request: Request):
    return await request.form()


@app.get("/alive")
async def alive() -> dict:
    return {
        "twilio_number": TWILIO_PHONE_NUMBER,
        "status": "alive"
    }


@app.post("/twilio-webhook")
def twilio_webhook(background_tasks: BackgroundTasks, request = Depends(get_request_form)) -> dict:
    sender_phone_number = request["From"]
    message_body = request["Body"]
    message_type = request["MessageType"]

    send_message(sender_phone_number, f"IA: {message_body}")

    return {
        "status": "Message sent",
        "number": sender_phone_number,
        "message_type": message_type,
    }

"""
https://platform.openai.com/docs/guides/function-calling
"""