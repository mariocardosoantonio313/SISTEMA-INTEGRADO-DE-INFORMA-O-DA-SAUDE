from __future__ import annotations

import hashlib


def hash_password(password: str) -> str:
    salt = hashlib.sha256()
    salt.update(password.encode("utf-8"))
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.digest(), 100000)
    return salt.hexdigest() + ":" + digest.hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if ":" not in hashed_password:
        return False
    salt_hex, stored_hash = hashed_password.split(":", 1)
    salt = bytes.fromhex(salt_hex)
    computed = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100000).hex()
    return computed == stored_hash
