import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

# Render Environment నుంచి API Key తీసుకోవడం
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/", methods=["GET"])
def home():
    return "AI Bot is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    user_msg = request.values.get('Body', '').strip()
    
    # Gemini AI ద్వారా ఆన్సర్ జనరేట్ చేయడం
    try:
        response = model.generate_content(f"You are a helpful and polite AI assistant on WhatsApp. Reply concisely: {user_msg}")
        bot_reply = response.text
    except Exception as e:
        bot_reply = "సారీ, ప్రస్తుతం సమాధానం ఇవ్వడంలో చిన్న సాంకేతిక సమస్య వచ్చింది."

    # Twilio కి రెస్పాన్స్ పంపడం
    resp = MessagingResponse()
    resp.message(bot_reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
