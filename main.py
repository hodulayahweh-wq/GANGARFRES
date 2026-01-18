from flask import Flask, jsonify, request
import json
import re

app = Flask(__name__)

API_KEY = "lord2026"

with open("api.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def normalize_gsm(gsm):
    gsm = re.sub(r"\D", "", gsm)
    if gsm.startswith("90"):
        gsm = gsm[2:]
    if gsm.startswith("0"):
        gsm = gsm[1:]
    return gsm

def check_key():
    key = request.args.get("key")
    return key == API_KEY

@app.route("/")
def home():
    return {"status": "API çalışıyor", "protected": True}

@app.route("/api/gsm/<gsm>")
def gsm_to_tc(gsm):
    if not check_key():
        return {"error": "Geçersiz API key"}, 401

    g = normalize_gsm(gsm)
    for r in data:
        if normalize_gsm(r.get("gsm", "")) == g:
            return jsonify(r)
    return {"error": "GSM bulunamadı"}, 404

@app.route("/api/tc/<tc>")
def tc_to_gsm(tc):
    if not check_key():
        return {"error": "Geçersiz API key"}, 401

    for r in data:
        if r.get("tc") == tc:
            return jsonify(r)
    return {"error": "TC bulunamadı"}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
