from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>AI Social Media Automation</h1>
    <p>Server is running successfully.</p>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "success",
        "message": "Server Running"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)