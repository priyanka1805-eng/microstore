from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from commonn.db import get_connection

app = Flask(__name__)

# -----------------------------
# REGISTER
# -----------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email=%s;", (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    hashed = generate_password_hash(password)
    cur.execute(
        "INSERT INTO users (email, password_hash, wallet_balance) VALUES (%s, %s, 0) RETURNING id;",
        (email, hashed)
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE email=%s;", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or not check_password_hash(user[1], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Simply return success message
    return jsonify({"message": "Login successful", "user_id": user[0]})

# -----------------------------
# LIST USERS (for testing)
# -----------------------------
@app.route("/users", methods=["GET"])
def users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, wallet_balance FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"id": u[0], "email": u[1], "wallet_balance": float(u[2])} for u in users])

if __name__ == "__main__":
    app.run(port=5001, debug=True)
