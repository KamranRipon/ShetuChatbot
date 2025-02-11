from flask_login import LoginManager
import transformers
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer 
import torch
import emotions
from flask_cors import CORS  # Import CORS
#from flask_sqlalchemy import SQLAlchemy
#from auth import auth_blueprint
import os  # Add this import



tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

app = Flask (__name__)
CORS(app, origins=["https://emotion-analysing-app.netlify.app/"])  # Allow only specific origins
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# db = SQLAlchemy(app)
# login_user = LoginManager(app)
# login_user.login_view = 'auth.login'
# # Register the blueprint
# app.register_blueprint(auth_blueprint)
@app.after_request
def add_security_headers(response):
    # Add the X-Content-Type-Options header
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"]) ##methods=["GET", "POST"]
def chat():
    msg = request.form['msg']
    # input = msg
    # return get_Chat_response(input)
    print(f"Received message from client: {msg}")  # Debugging: log the message from the user

    response = get_Chat_response(msg)
    # response = emotions.get_response(msg)
    print(f"Bot response: {response}")  # Debugging: log the bot's response
    return jsonify(response)  # Make sure to return JSON or a simple string
    #return response


def get_Chat_response(text):

# Let's chat for 5 lines
    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        return (tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))
    


# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000
    app.run(host="0.0.0.0", port=port)  # Bind to 0.0.0.0 and the specified port