import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API Key from environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Set up Gemini model with updated version name
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    system_instruction="You are a polite and helpful AI assistant for IV Intelligence on WhatsApp. Reply concisely."
)

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    if not incoming_msg:
        resp.message("Hello! How can I help you today?")
        return str(resp)

    try:
        # Generate AI response
        response = model.generate_content(incoming_msg)
        reply_text = response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        reply_text = "Sorry, I encountered an issue processing your message."

    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


