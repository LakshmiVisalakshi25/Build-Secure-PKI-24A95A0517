import base64
import pyotp

def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-character hex seed to base32 string
    """
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes)
    return base32_seed.decode('utf-8')


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP code from hex seed
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with ±valid_window periods (default ±30s)
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)


# Example usage
if __name__ == "__main__":
    # Load seed from file
    with open("data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    totp_code = generate_totp_code(hex_seed)
    print("Current TOTP Code:", totp_code)

    is_valid = verify_totp_code(hex_seed, totp_code)
    print("Is code valid?", is_valid)
