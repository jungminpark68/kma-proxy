from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔐 여기 인증키 하드코딩 (네가 주던 공용키)
AUTH_KEY = "wLWQLTOfRxC1kC0zn7cQ2g"

@app.route('/kma-ultra')
def kma_proxy():
    url = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"

    # 클라이언트(HTML)에서는 authKey 안 보내도 됨
    base_date = request.args.get("base_date")
    base_time = request.args.get("base_time")
    nx        = request.args.get("nx")
    ny        = request.args.get("ny")

    params = {
        "authKey": AUTH_KEY,
        "dataType": "JSON",
        "numOfRows": 100,
        "pageNo": 1,
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }

    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "KMA Proxy Server OK!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
