import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

# Gemini API Key సెటప్
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/", methods=['GET'])
def home():
    return "IV Intelligence WhatsApp Bot is Live!"

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    if not incoming_msg:
        resp.message("హలో! నేను మీకు ఎలా సహాయపడగలను?")
        return str(resp)

    try:
        response = model.generate_content(incoming_msg)
        reply_text = response.text
    except Exception as e:
        print(f"Error: {e}")
        reply_text = "క్షమించండి, ప్రస్తుతం ప్రతిస్పందించలేకపోతున్నాను."

    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
