import secrets
import string
import math

ALLOWED_LENGTHS = (8, 16, 32, 64)
JWT_DEFAULT_LENGTH = 64

UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SPECIAL = "!@#$%^&*()-_=+[]{}|;:,.<>?"
JWT_CHARS = UPPERCASE + LOWERCASE + DIGITS + "-_"

ALL_CHARS = UPPERCASE + LOWERCASE + DIGITS + SPECIAL


def generate_password(length: int = 16) -> str:
    if length not in ALLOWED_LENGTHS:
        raise ValueError(f"Length must be one of {ALLOWED_LENGTHS}")

    # Force at least one from each category
    password = [
        secrets.choice(UPPERCASE),
        secrets.choice(LOWERCASE),
        secrets.choice(DIGITS),
        secrets.choice(SPECIAL),
    ]

    # Fill the rest randomly from all chars
    for _ in range(length - 4):
        password.append(secrets.choice(ALL_CHARS))

    # Shuffle to avoid predictable positions
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def batch_generate(length: int = 16, count: int = 1) -> list[str]:
    return [generate_password(length) for _ in range(count)]


def generate_jwt_password(length: int = JWT_DEFAULT_LENGTH) -> str:
    if length < 16:
        raise ValueError("JWT password length must be at least 16")
    password = [
        secrets.choice(UPPERCASE),
        secrets.choice(LOWERCASE),
        secrets.choice(DIGITS),
    ]
    for _ in range(length - 3):
        password.append(secrets.choice(JWT_CHARS))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def batch_generate_jwt(count: int = 1, length: int = JWT_DEFAULT_LENGTH) -> list[str]:
    return [generate_jwt_password(length) for _ in range(count)]


def calc_entropy(password: str, is_jwt: bool = False) -> float:
    charset_size = 0
    if any(c in UPPERCASE for c in password):
        charset_size += len(UPPERCASE)
    if any(c in LOWERCASE for c in password):
        charset_size += len(LOWERCASE)
    if any(c in DIGITS for c in password):
        charset_size += len(DIGITS)
    if is_jwt:
        charset_size += 2  # - and _
    elif any(c in SPECIAL for c in password):
        charset_size += len(SPECIAL)
    if charset_size == 0:
        return 0.0
    return len(password) * math.log2(charset_size)


def strength_label(entropy: float) -> str:
    if entropy < 50:
        return "弱"
    elif entropy < 80:
        return "中等"
    elif entropy < 120:
        return "强"
    else:
        return "非常强"


def password_info(password: str, is_jwt: bool = False) -> dict:
    entropy = calc_entropy(password, is_jwt)
    return {
        "password": password,
        "length": len(password),
        "entropy": round(entropy, 1),
        "strength": strength_label(entropy),
    }
