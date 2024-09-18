from flask import Flask, render_template, request
import re
from textblob import TextBlob
import nltk

# Download punkt for TextBlob
nltk.download('punkt')

# Emotion-based dictionary
emotion_dict = {
    'sadness': ['sad', 'depressed', 'unhappy', 'down', 'heartbroken', 'miserable'],
    'anger': ['angry', 'mad', 'frustrated', 'furious', 'upset', 'irritated'],
    'joy': ['happy', 'joyful', 'excited', 'thrilled', 'content'],
    'anxiety': ['anxious', 'nervous', 'worried', 'concerned', 'afraid'],
}

# Sentiment analysis using TextBlob
def analyze_sentiment(user_input):
    blob = TextBlob(user_input)
    sentiment = blob.sentiment.polarity
    return sentiment

# Emotion recognition based on keywords
def detect_emotion(user_input):
    for emotion, keywords in emotion_dict.items():
        if any(word in user_input for word in keywords):
            return emotion
    return None

# Initialize Flask app
app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Chatbot route for handling user input
@app.route('/get', methods=['POST'])
def chatbot_response():
    user_input = request.form['msg'].strip().lower()
    
    # Remove common greeting words
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    for greeting in greetings:
        if user_input.startswith(greeting):
            user_input = user_input.replace(greeting, "").strip()
            break

    # Analyze sentiment and detect emotion
    sentiment = analyze_sentiment(user_input)
    emotion = detect_emotion(user_input)
    
    # Respond based on detected emotions
    if emotion == 'sadness':
        return f"I'm sorry you're feeling sad. Do you want to talk more about what's making you feel this way?"
    elif emotion == 'anger':
        return f"It sounds like you're upset. What do you think is causing your anger?"
    elif emotion == 'joy':
        return f"I'm happy to hear you're feeling good! What's been making you feel joyful?"
    elif emotion == 'anxiety':
        return f"It sounds like you're feeling anxious. Would you like to share what's worrying you?"
    else:
        # Sentiment-based fallback responses
        if sentiment < -0.3:
            return "I can sense you're feeling down. Do you want to talk more about what’s troubling you?"
        elif sentiment > 0.3:
            return "You seem to be in a good mood! What’s making you feel this way?"
        else:
            return "I’m here to understand. Could you explain a bit more about what’s on your mind?"

if __name__ == "__main__":
    app.run(debug=True)

    