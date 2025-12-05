import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP(SHA-256)
    Returns HEX seed (64 chars)
    """

    # 1. Base64 decode
    ciphertext = base64.b64decode(encrypted_seed_b64)

    # 2. RSA OAEP decrypt
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Convert decrypted bytes -> UTF-8 string
    seed_hex = plaintext_bytes.decode("utf-8")

    # 4. Validate: must be 64-character lowercase hex
    if len(seed_hex) != 64:
        raise ValueError("Invalid seed length — expected 64 hex characters")

    valid_hex_chars = set("0123456789abcdef")
    if not all(c in valid_hex_chars for c in seed_hex):
        raise ValueError("Seed contains invalid characters. Must be hex.")

    return seed_hex


def load_private_key():
    with open("student_private.pem", "rb") as f:
        key_data = f.read()

    private_key = serialization.load_pem_private_key(
        key_data,
        password=None
    )
    return private_key


if __name__ == "__main__":
    # Load encrypted seed
    with open("encrypted_seed.txt", "r") as f:
        encrypted_b64 = f.read().strip()

    # Load private key
    priv_key = load_private_key()

    # Decrypt
    seed = decrypt_seed(encrypted_b64, priv_key)

    print("Decrypted Seed:", seed)

    # Ensure 'data' folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Save decrypted seed to 'data/seed.txt' (visible in VS Code)
    with open("data/seed.txt", "w") as f:
        f.write(seed)

    print("Seed saved to data/seed.txt")
