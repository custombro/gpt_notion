from flask import Flask, jsonify
import os
from automation_handler import run_automation_engine

app = Flask(__name__)

# 기본 페이지
@app.route("/")
def home():
    return "Server is running.", 200

# 헬스 체크
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# 디버그
@app.route("/debug")
def debug():
    cwd = os.getcwd()
    files = os.listdir(cwd)
    return jsonify({"cwd": cwd, "files": files}), 200

# ✅ 자동화 실행 API (Render가 이걸 호출하게 됨)
@app.route("/run_automation")
def run_auto():
    result = run_automation_engine()
    return jsonify(result), 200


if __name__ == "__main__":
    # Render에서는 절대 사용 안함 (로컬 테스트용)
    app.run(host="0.0.0.0", port=5000)
