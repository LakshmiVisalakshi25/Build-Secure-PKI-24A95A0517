#!/usr/bin/env python3
import subprocess
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key(path="student_private.pem"):
    with open(path, "rb") as f:
        key_data = f.read()
    return serialization.load_pem_private_key(key_data, password=None)

def sign_message(message: str, private_key) -> bytes:
    msg_bytes = message.encode("utf-8")
    return private_key.sign(
        msg_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def load_public_key(path="instructor_public.pem"):
    with open(path, "rb") as f:
        key_data = f.read()
    return serialization.load_pem_public_key(key_data)

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def base64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")

if __name__ == "__main__":
    # 1. Get current commit hash
    commit_hash = subprocess.check_output(["git", "log", "-1", "--format=%H"]).decode("utf-8").strip()
    print("Commit Hash:", commit_hash)

    # 2. Load student private key
    private_key = load_private_key()

    # 3. Sign commit hash
    signature = sign_message(commit_hash, private_key)

    # 4. Load instructor public key
    instructor_pub = load_public_key()

    # 5. Encrypt signature
    encrypted_sig = encrypt_with_public_key(signature, instructor_pub)

    # 6. Base64 encode
    encrypted_sig_b64 = base64_encode(encrypted_sig)
    print("Encrypted Signature (Base64):", encrypted_sig_b64)
