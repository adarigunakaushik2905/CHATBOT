from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# -------- OLLAMA CONFIG --------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"

# -------- MONGODB CONFIG --------
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]          # database name
collection = db["chats"]           # collection name

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    payload = {
        "model": MODEL_NAME,
        "prompt": user_message,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 120
        }
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        return jsonify({"reply": "❌ Ollama error"}), 500

    result = response.json()
    bot_reply = result.get("response", "")

    # -------- STORE IN NOSQL DB --------
    chat_doc = {
        "user_message": user_message,
        "bot_reply": bot_reply,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(chat_doc)

    return jsonify({"reply": bot_reply})

# -------- FETCH CHAT HISTORY (OPTIONAL) --------
@app.route("/history", methods=["GET"])
def history():
    chats = list(collection.find({}, {"_id": 0}))
    return jsonify(chats)

if __name__ == "__main__":
    app.run(debug=True)
