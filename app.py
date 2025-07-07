from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for external access (e.g. from Cloudflare Pages)

# Path to JSON data file
DATA_FILE = "data/data.json"

# Ensure the data directory and JSON file exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({
            "from": "",
            "network": "Ethereum",
            "amount": "",
            "to": "",
            "Txnhash": ""
        }, f, indent=2)

# Load data from JSON
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save data to JSON
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Home page (Metamask-style view)
@app.route("/")
def home():
    return render_template("metamask.html", data=load_data())

# Admin panel
@app.route("/admin", methods=["GET", "POST"])
def admin():
    data = load_data()
    if request.method == "POST":
        data["from"] = request.form["from"]
        data["network"] = request.form["network"]
        data["amount"] = request.form["amount"]
        data["to"] = request.form["to"]
        data["Txnhash"] = request.form["Txnhash"]
        save_data(data)
        return redirect(url_for("admin"))
    return render_template("admin.html", data=data)

# Metamask page
@app.route("/metamask")
def metamask():
    return render_template("metamask.html", data=load_data())

# Receipt page
@app.route("/receipt")
def receipt():
    return render_template("receipt.html", data=load_data())

# ✅ NEW: API endpoint to return JSON for Cloudflare Pages
@app.route("/api/data")
def api_data():
    return jsonify(load_data())

# Run app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  # ✅ Explicitly define host and port for Replit
