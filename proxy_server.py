from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/kma-ultra')
def kma_proxy():
    url = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"

    params = {
        "authKey": request.args.get("authKey"),
        "dataType": "JSON",
        "numOfRows": 100,
        "pageNo": 1,
        "base_date": request.args.get("base_date"),
        "base_time": request.args.get("base_time"),
        "nx": request.args.get("nx"),
        "ny": request.args.get("ny")
    }

    resp = requests.get(url, params=params)
    return jsonify(resp.json())

@app.route("/")
def home():
    return "KMA Proxy Server OK!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
