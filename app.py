from flask import Flask, request
from automation_handler import run_automation

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ GPT-AUTO-NOTION SERVER RUNNING"

@app.route("/run", methods=["GET"])
def run():
    result = run_automation()
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
