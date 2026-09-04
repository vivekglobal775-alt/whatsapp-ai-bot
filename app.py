import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is Running Live!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    resp.message("Hi! AI Sales Bot is working fine.")
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
