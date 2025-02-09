from flask import Flask, render_template, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

# Predefined responses for different sentiments
POSITIVE_RESPONSES = [
    "That's great to hear! 😊",
    "I'm so happy for you! 🎉",
    "Keep up the good work, you're doing amazing!"
]

NEGATIVE_RESPONSES = [
    "I'm really sorry to hear that. 😢",
    "It sounds like you're going through a tough time.",
    "I'm here if you need to talk more."
]

NEUTRAL_RESPONSES = [
    "I see. What else would you like to talk about?",
    "Got it. Let me know if there's something specific on your mind.",
    "Okay. Anything else you'd like to share?"
]

def analyze_sentiment(text):
    # Use TextBlob to analyze the sentiment of the input text
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity  # Returns a value between -1 and 1
    
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

def get_response(sentiment):
    # Return a response based on the sentiment
    if sentiment == "positive":
        return POSITIVE_RESPONSES
    elif sentiment == "negative":
        return NEGATIVE_RESPONSES
    else:
        return NEUTRAL_RESPONSES

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_chatbot_response():
    user_message = request.json['message']
    sentiment = analyze_sentiment(user_message)
    responses = get_response(sentiment)
    
    # Return a random response from the appropriate list
    return jsonify(response=responses[0])

if __name__ == '__main__':
    app.run(debug=True)
