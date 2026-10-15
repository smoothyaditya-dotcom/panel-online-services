import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BASE_URL = "https://panel-online-services.onrender.com"

PRODUCTS = [
    {
        "id": 1,
        "name": "Panel",
        "price": "₹20",
        "image": BASE_URL + "/static/panel_artwork.jpg",
        "live": True,
        "upi_link": "upi://pay?pa=7276052050@fam&pn=PANEL%20OFFICIAL&am=20.00&cu=INR&tn=Panel%20Payment",
        "qr": "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=upi%3A%2F%2Fpay%3Fpa%3D7276052050%40fam%26pn%3DPANEL%2520OFFICIAL%26am%3D20.00%26cu%3DINR%26tn%3DPanel%2520Payment",
    },
    {
        "id": 2,
        "name": "Panel Pro",
        "price": "₹25",
        "image": BASE_URL + "/static/panel_artwork.jpg",
        "live": True,
        "upi_link": "upi://pay?pa=7276052050@fam&pn=PANEL%20OFFICIAL&am=25.00&cu=INR&tn=Panel%20Pro%20Payment",
        "qr": "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=upi%3A%2F%2Fpay%3Fpa%3D7276052050%40fam%26pn%3DPANEL%2520OFFICIAL%26am%3D25.00%26cu%3DINR%26tn%3DPanel%2520Pro%2520Payment",
    },
    {
        "id": 3,
        "name": "Panel Premium",
        "price": "₹30",
        "image": BASE_URL + "/static/panel_artwork.jpg",
        "live": True,
        "upi_link": "upi://pay?pa=7276052050@fam&pn=PANEL%20OFFICIAL&am=30.00&cu=INR&tn=Panel%20Premium%20Payment",
        "qr": "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=upi%3A%2F%2Fpay%3Fpa%3D7276052050%40fam%26pn%3DPANEL%2520OFFICIAL%26am%3D30.00%26cu%3DINR%26tn%3DPanel%2520Premium%2520Payment",
    },
]

ORDERS_FILE = "orders.txt"

@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)

@app.route("/save_order", methods=["POST"])
def save_order():
    data = request.get_json() or {}
    name = str(data.get("customer_name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    addr = str(data.get("address", "")).strip()
    prod = str(data.get("product", "")).strip()
    prc = str(data.get("price", "")).strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = "-" * 40 + "\n"
    entry += f"Time: {now}\n"
    entry += f"Product: {prod} ({prc})\n"
    entry += f"Name: {name}\n"
    entry += f"Phone: {phone}\n"
    entry += f"Address: {addr}\n"
    entry += "-" * 40 + "\n\n"

    with open(ORDERS_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    return jsonify({"status": "ok"})

@app.route("/orders")
def view_orders():
    if not os.path.exists(ORDERS_FILE):
        return "<pre style='background:#111;color:#eee;padding:20px;'>No orders received yet.</pre>"
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    return f"<pre style='background:#111;color:#76ff03;padding:20px;font-family:monospace;white-space:pre-wrap;'>{content}</pre>"

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)
    
