import base64
import cv2
import numpy as np
import hashlib
from deepface import DeepFace

# -------------------------------
# Convert base64 image to OpenCV image
# -------------------------------
def base64_to_image(base64_str):
    base64_str = base64_str.split(",")[1]
    img_bytes = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

# -------------------------------
# Generate FaceNet embedding
# -------------------------------
def generate_embedding(base64_image):
    img = base64_to_image(base64_image)

    result = DeepFace.represent(
        img_path=img,
        model_name="Facenet",
        enforce_detection=True
        
    )
    embedding = np.array(result[0]["embedding"], dtype=np.float32)
    print("Embedding length:", len(embedding)) 
    return embedding

# -------------------------------
# Generate stable hash from embedding
# (Used for DB + Blockchain integrity)
# -------------------------------
def generate_embedding_hash(embedding):
    stable_embedding = np.round(embedding, 2)   # VERY IMPORTANT
    hash_value = hashlib.sha256(stable_embedding.tobytes()).hexdigest()
    return hash_value

# -------------------------------
# Cosine distance for verification
# -------------------------------
def cosine_distance(vec1, vec2):
    return 1 - np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

