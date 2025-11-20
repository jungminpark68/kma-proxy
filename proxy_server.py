# proxy_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # 모든 origin 허용 (file://, http://localhost 등)

AUTH_KEY = "wLWQLTOfRxC1kC0zn7cQ2g"  # 네가 준 공용 키

@app.get("/kma-ultra")
def kma_ultra():
    base_date = request.args.get("base_date")
    base_time = request.args.get("base_time")
    nx = request.args.get("nx")
    ny = request.args.get("ny")

    if not (base_date and base_time and nx and ny):
        return jsonify({"error": "base_date, base_time, nx, ny 필수"}), 400

    url = (
        "https://apihub.kma.go.kr/api/typ02/openApi/"
        "VilageFcstInfoService_2.0/getUltraSrtNcst"
    )
    params = {
        "authKey": AUTH_KEY,
        "dataType": "JSON",
        "numOfRows": 100,
        "pageNo": 1,
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
    except Exception as e:
        return jsonify({"error": "KMA request failed", "detail": str(e)}), 502

    return jsonify(r.json())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
