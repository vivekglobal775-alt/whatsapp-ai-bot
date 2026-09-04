import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
@app.route('/', methods=['GET'])
def home():
    return "Server is Running Live!", 200

app = Flask(__name__))

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    # AI Bot Auto-Response Logic
    if incoming_msg.lower() in ['hi', 'hello', 'namaste']:
        msg.body("నమస్కారం! AI అసిస్టెంట్‌కి స్వాగతం. నేను మీకు ఎలా సహాయపడగలను?")
    else:
        msg.body(f"మీ మెసేజ్ అందింది: '{incoming_msg}'. మన AI సర్వర్ త్వరలోనే పూర్తి వివరాలతో రిప్లై ఇస్తుంది!")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
