from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
from decrypt_seed import decrypt_seed, load_private_key
from totp_utils import generate_totp_code, verify_totp_code
import base64
import time

app = FastAPI()

DATA_PATH = "data/seed.txt"

# -------------------------------
# Pydantic models for requests
# -------------------------------

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str

# -------------------------------
# Endpoint 1: POST /decrypt-seed
# -------------------------------

@app.post("/decrypt-seed")
def post_decrypt_seed(req: DecryptSeedRequest):
    try:
        # Load private key
        priv_key = load_private_key()

        # Decrypt
        seed_hex = decrypt_seed(req.encrypted_seed, priv_key)

        # Ensure data folder exists
        if not os.path.exists("data"):
            os.makedirs("data")

        # Save decrypted seed
        with open(DATA_PATH, "w") as f:
            f.write(seed_hex)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": f"Decryption failed: {str(e)}"})


# -------------------------------
# Endpoint 2: GET /generate-2fa
# -------------------------------

@app.get("/generate-2fa")
def get_generate_2fa():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    with open(DATA_PATH, "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)

    # Calculate remaining seconds in current 30s period
    period = 30
    valid_for = period - (int(time.time()) % period)

    return {"code": code, "valid_for": valid_for}


# -------------------------------
# Endpoint 3: POST /verify-2fa
# -------------------------------

@app.post("/verify-2fa")
def post_verify_2fa(req: Verify2FARequest):
    if not req.code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})

    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    with open(DATA_PATH, "r") as f:
        hex_seed = f.read().strip()

    is_valid = verify_totp_code(hex_seed, req.code)

    return {"valid": is_valid}
