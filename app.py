
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

# API Key Check
api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.route("/", methods=['GET'])
def home():
    return "IV Intelligence WhatsApp Bot is Live!", 200

@app.route("/webhook", methods=['POST'])
def webhook():
    resp = MessagingResponse()
    incoming_msg = request.values.get('Body', '').strip()

    if not api_key:
        resp.message("IV Error: Render లో GOOGLE_API_KEY మిస్ అయ్యింది!")
        return str(resp)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(incoming_msg)
        reply_text = response.text if response.text else "సారీ, రెస్పాన్స్ పొందలేకపోయాను."
    except Exception as e:
        reply_text = f"IV Intelligence Error: {str(e)}"

    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
