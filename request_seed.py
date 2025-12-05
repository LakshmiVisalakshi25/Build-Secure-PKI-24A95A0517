import json
import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
STUDENT_ID = "24A95A0517"
GITHUB_REPO_URL = "https://github.com/LakshmiVisalakshi25/Build-Secure-PKI-24A95A0517"

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    # 1. Read student public key from PEM file
    with open("student_public.pem", "r") as f:
        public_key_pem = f.read()

    # 2. Prepare JSON payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_pem
    }

    # 3. Send POST request
    response = requests.post(api_url, json=payload, timeout=20)

    # 4. Parse response
    data = response.json()
    if "encrypted_seed" not in data:
        print("Error:", data)
        return

    encrypted_seed = data["encrypted_seed"]

    # 5. Save encrypted seed to file
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("Encrypted seed saved to encrypted_seed.txt")

if __name__ == "__main__":
    request_seed(STUDENT_ID, GITHUB_REPO_URL, API_URL)
