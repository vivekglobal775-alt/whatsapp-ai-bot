import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

# Render Environment నుంచి API Key సెటప్
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY కనుగొనబడలేదు!", flush=True)

# System Instruction తో మోడల్ కాన్ఫిగరేషన్
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are a helpful and polite AI assistant on WhatsApp. Reply concisely."
)

@app.route("/", methods=["GET"])
def home():
    return "AI Bot is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    user_msg = request.values.get('Body', '').strip()
    print(f"వచ్చిన మెసేజ్: {user_msg}", flush=True)
    
    try:
        # Gemini AI ద్వారా రెస్పాన్స్ జనరేట్ చేయడం
        response = model.generate_content(user_msg)
        
        if response and response.text:
            bot_reply = response.text
        else:
            bot_reply = "సారీ, సరైన సమాధానం జెనరేట్ అవ్వలేదు."
            
    except Exception as e:
        # Render Logs లో అసలు కారణం ప్రింట్ అవ్వడానికి ఇది సహాయపడుతుంది
        print(f"!!! GEMINI ERROR !!!: {e}", flush=True)
        bot_reply = "సారీ, ప్రస్తుతం సమాధానం ఇవ్వడంలో చిన్న సాంకేతిక సమస్య వచ్చింది."

    # Twilio ద్వారా రెస్పాన్స్ పంపడం
    resp = MessagingResponse()
    resp.message(bot_reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

