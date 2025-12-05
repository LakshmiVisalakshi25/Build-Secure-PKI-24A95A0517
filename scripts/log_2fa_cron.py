#!/usr/bin/env python3
# Cron script to log 2FA codes every minute

import os
from datetime import datetime, timezone
from totp_utils import generate_totp_code

SEED_FILE = "/data/seed.txt"

def main():
    # 1. Read hex seed from persistent storage
    try:
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()
    except FileNotFoundError:
        print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} - Seed file not found")
        return

    # 2. Generate current TOTP code
    code = generate_totp_code(hex_seed)

    # 3. Get current UTC timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # 4. Output formatted line
    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
