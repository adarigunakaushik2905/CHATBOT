from flask import Flask, render_template, request, jsonify
from sambanova import SambaNova

app = Flask(__name__)

# ✅ API key (direct for now)
client = SambaNova(
    api_key="8807ef7a-77c5-4d01-93cd-cd7c25997674",
    base_url="https://api.sambanova.ai/v1"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data["message"]

        print("User:", user_message)

        response = client.chat.completions.create(
            model="Qwen3-235B",  
            messages=[
                {"role": "system", "content": "You are a helpful AI chatbot."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            top_p=0.9
        )

        bot_reply = response.choices[0].message.content
        print("Bot:", bot_reply)

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "❌ Model error. Check terminal."})

if __name__ == "__main__":
    app.run(debug=True)
