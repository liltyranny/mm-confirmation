from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

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

# Utility: Load data from JSON
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Utility: Save data to JSON
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Homepage - will show the main Metamask-style page
@app.route("/")
def home():
    return render_template("metamask.html", data=load_data())

# Admin panel for updating values
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

# Dedicated route to metamask page (optional, since home uses it)
@app.route("/metamask")
def metamask():
    return render_template("metamask.html", data=load_data())

# Receipt page
@app.route("/receipt")
def receipt():
    return render_template("receipt.html", data=load_data())

# Run app
if __name__ == "__main__":
    app.run(debug=True)
