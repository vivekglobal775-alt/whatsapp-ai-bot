
import os
import threading
from flask import Flask, request
from twilio.rest import Client
import google.generativeai as genai

app = Flask(__name__)

# 1. Secure Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Prevent Duplicate Processing
processed_sids = set()

def process_message_async(incoming_msg, sender_number, recipient_number, message_sid):
    # Check duplicate retries
    if message_sid in processed_sids:
        print(f"[INFO] MessageSid {message_sid} already processed. Skipping.")
        return

    processed_sids.add(message_sid)
    print(f"[INFO] Asynchronously processing MessageSid: {message_sid}")

    # 2. Call Gemini API
    reply_text = ""
    if not GEMINI_API_KEY:
        reply_text = "IV Error: GEMINI_API_KEY is not configured in environment variables."
        print("[ERROR] Missing Gemini API Key")
    else:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(incoming_msg)
            reply_text = response.text if response.text else "సారీ, రెస్పాన్స్ పొందలేకపోయాను."
        except Exception as e:
            reply_text = f"IV Intelligence AI Error: {str(e)}"
            print(f"[ERROR] Gemini generation failed: {str(e)}")

    # 3. Send Response via Twilio REST API
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN):
        print("[ERROR] Missing Twilio Account SID or Auth Token.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=reply_text,
            from_=recipient_number,  # Twilio WhatsApp number
            to=sender_number         # User WhatsApp number
        )
        print(f"[SUCCESS] Sent async response for MessageSid: {message_sid}")
    except Exception as e:
        print(f"[ERROR] Twilio REST API failed to send message: {str(e)}")


@app.route("/", methods=['GET'])
def home():
    return "IV Intelligence Async Server is Live!", 200


@app.route("/webhook", methods=['POST'])
def webhook():
    message_sid = request.values.get('MessageSid', '')
    incoming_msg = request.values.get('Body', '').strip()
    sender_number = request.values.get('From', '')
    recipient_number = request.values.get('To', '')

    # Spawn async background job
    thread = threading.Thread(
        target=process_message_async,
        args=(incoming_msg, sender_number, recipient_number, message_sid)
    )
    thread.start()

    # Immediately respond to Twilio with HTTP 200 (No timeout)
    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
