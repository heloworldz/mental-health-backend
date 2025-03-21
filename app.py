import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

responses = {
    "positive": ["That's great to hear! Keep it up!", "You're doing awesome!"],
    "neutral": ["I see. Tell me more.", "Interesting, go on."],
    "negative": ["I'm here for you. You’re not alone.", "Consider talking to a friend or professional."]
}

def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    print(f"Sentiment Score: {sentiment}")  # Debugging line

    if sentiment >= 0.1:  # 🔹 Make threshold lower
        return "positive"
    elif sentiment <= -0.1:  # 🔹 Make threshold lower
        return "negative"
    else:
        return "neutral"


@app.route("/")
def home():
    return "Backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    sentiment = analyze_sentiment(user_input)
    response = random.choice(responses[sentiment])
    return jsonify({"response": response, "sentiment": sentiment})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Ensure Render's PORT is used
    app.run(host="0.0.0.0", port=port)  # 🔴 REMOVE debug=True (not needed in production)
