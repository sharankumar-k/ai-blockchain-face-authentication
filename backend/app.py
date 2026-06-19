from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import bcrypt

from face_ai import (
    generate_embedding,
    generate_embedding_hash,
    cosine_distance
)

from database import (
    init_db,
    store_user,
    get_user,
    user_exists
)

from blockchain import (
    register_face_hash,
    verify_face_hash
)

# -----------------------------------
# App setup
# -----------------------------------
app = Flask(__name__)
CORS(app)

# ✅ Frontend folder
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Initialize database
init_db()

# FaceNet recommended threshold
THRESHOLD = 0.25

# -----------------------------------
# ✅ Serve Frontend properly
# -----------------------------------
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/script.js")
def script():
    return send_from_directory(FRONTEND_DIR, "script.js")


# -----------------------------------
# REGISTER ✅ (Duplicate blocked)
# -----------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    email = data.get("email")
    password = data.get("password")
    image = data.get("image")

    if not email or not password or not image:
        return jsonify({"message": "Missing required fields"}), 400

    # ✅ Check if user already exists
    if user_exists(email):
        return jsonify({"message": "User already exists. Please verify/login."}), 409

    # Generate embedding
    embedding = generate_embedding(image)

    # Generate stable hash
    face_hash = generate_embedding_hash(embedding)

    # Store in database

    hashed_password = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()).decode('utf-8')
    store_user(email, hashed_password, embedding, face_hash)
    
    # Store hash on blockchain
    register_face_hash(email, face_hash)

    return jsonify({"message": "User registered successfully"}), 200


# -----------------------------------
# VERIFY
# -----------------------------------
@app.route("/verify", methods=["POST"])
def verify():
    data = request.json

    email = data.get("email")
    password = data.get("password")
    image = data.get("image")

    if not email or not password or not image:
        return jsonify({"message": "Missing required fields"}), 400

    # Fetch stored data
    stored_password, stored_embedding, stored_hash = get_user(email)

    if stored_password is None:
        return jsonify({"message": "User not found"}), 404

    # Password check
    if not bcrypt.checkpw(
    password.encode('utf-8'),
    stored_password.encode('utf-8')):
        return jsonify({"message": "Invalid password"}), 401

    # Integrity check (DB ↔ Blockchain)
    if not verify_face_hash(email, stored_hash):
        return jsonify({"message": "Integrity violation detected"}), 403

    # Generate live embedding
    live_embedding = generate_embedding(image)

    # Distance-based verification
    distance = cosine_distance(stored_embedding, live_embedding)
    distance_value = float(round(distance, 3))
    print("Distance:", distance_value)
    if distance_value < THRESHOLD:
        return jsonify({
            "message": "Face verified successfully",
            "distance": distance_value
        }), 200
    else:
        return jsonify({
            "message": "Face verification failed",
            "distance": distance_value
        }), 401


# -----------------------------------
# Run server
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
