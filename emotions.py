from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from flask_cors import CORS
import random
import re


 # Allow only specific origins

# Small Talk Responses
SMALL_TALK_RESPONSES = [
    "Hello! How can I assist you today?",
    "Hey there! What’s on your mind?",
    "Hi! What can I do for you?",
    "Greetings! How can I help?"
]

# Personal Questions About the Bot
BOT_RESPONSES = {
    "how are you": ["I'm just a bot, but I'm doing great! 😊", "I don't have feelings, but I'm here to chat!"],
    "what is your name": ["I'm your friendly chatbot!", "Call me ChatBuddy!"],
    "what can you do": ["I can analyze emotions and chat with you!", "I try my best to be a helpful assistant."],
    "who are you": ["I'm your AI-powered chatbot here to help!", "I'm ChatBuddy, your virtual assistant."]
}

# Sentiment-Based Responses
POSITIVE_RESPONSES = [
    "That's great to hear! 😊",
    "I'm happy for you! 🎉",
    "Keep up the good vibes!",
    "Awesome! Let me know if there's anything else I can do."
]

NEGATIVE_RESPONSES = [
    "I'm sorry you're feeling this way. 😢",
    "That sounds tough. Do you want to talk about it?",
    "I'm here for you if you need support.",
    "I understand. You’re not alone in this."
]

NEUTRAL_RESPONSES = [
    "I see. What else is on your mind?",
    "Got it. Let me know if there's something specific you’d like to discuss.",
    "Interesting! Tell me more about it.",
    "Okay. Anything else you'd like to share?"
]

# Fallback Responses
FALLBACK_RESPONSES = [
    "I'm not sure I understand. Can you rephrase that?",
    "Hmm, I’m not sure what you mean. Could you elaborate?",
    "I’m still learning! Could you clarify that for me?"
]

# Keywords for small talk detection
SMALL_TALK_PATTERNS = re.compile(r"\b(hello|hi|hey|greetings|howdy|sup|what's up)\b", re.IGNORECASE)
BOT_QUESTION_PATTERNS = re.compile(r"\b(how are you|what is your name|who are you|what can you do)\b", re.IGNORECASE)
QUESTION_PATTERN = re.compile(r"\?$")  # Detects if input is a question

# Context tracker
user_context = {}

def analyze_sentiment(text):
    """Analyze the sentiment of a given text and classify it."""
    try:
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        if polarity > 0.3:
            return "positive", polarity
        elif polarity < -0.3:
            return "negative", polarity
        else:
            return "neutral", polarity
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "neutral", 0

def get_response(sentiment, user_message, polarity):
    """Generate an appropriate response based on sentiment, message content, and polarity."""
    
    # Check if the user is asking a small talk or chatbot-related question
    if BOT_QUESTION_PATTERNS.search(user_message):
        for key, responses in BOT_RESPONSES.items():
            if key in user_message:
                return random.choice(responses)
    
    # If message is a question, adjust response
    if QUESTION_PATTERN.search(user_message):
        if sentiment == "positive":
            return "That sounds nice! Can you tell me more?"
        elif sentiment == "negative":
            return "I understand. Is there something I can do to help?"
        else:
            return "That's an interesting question. What do you think?"

    # General responses based on sentiment and polarity intensity
    if sentiment == "positive":
        if polarity > 0.6:
            return "Wow, that’s amazing! 😃"
        else:
            return random.choice(POSITIVE_RESPONSES)
    elif sentiment == "negative":
        if polarity < -0.6:
            return "That sounds really difficult. I’m here for you. 😢"
        else:
            return random.choice(NEGATIVE_RESPONSES)
    else:
        return random.choice(NEUTRAL_RESPONSES)

def get_chatbot_response(user_message):
    """Handles user input, detects type of message, and generates appropriate responses."""
    try:
        user_message = str(user_message).strip().lower()
        
        if not user_message:
            return "Please type something so I can respond!"

        # Handle small talk separately
        if SMALL_TALK_PATTERNS.search(user_message):
            return random.choice(SMALL_TALK_RESPONSES)

        # Analyze sentiment
        sentiment, polarity = analyze_sentiment(user_message)
        response = get_response(sentiment, user_message, polarity)

        # Fallback if no response is generated
        if not response:
            response = random.choice(FALLBACK_RESPONSES)

        # Debugging logs
        print(f"User: {user_message}")
        print(f"Sentiment: {sentiment}, Polarity: {polarity}")
        print(f"Bot Response: {response}")

        return response  # Return a string, not a dictionary or JSON object
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return "Sorry, something went wrong. Please try again!"
