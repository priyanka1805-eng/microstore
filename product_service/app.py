
from flask import Flask, jsonify, request
from common.db import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"service": "Product Service", "status": "running"})

@app.route("/products", methods=["GET"])
def get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, sku, name, price, stock FROM products;")
    products = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {"id": p[0], "sku": p[1], "name": p[2], "price": float(p[3]), "stock": p[4]}
        for p in products
    ])

if __name__ == "__main__":
    app.run(port=5002, debug=True)
