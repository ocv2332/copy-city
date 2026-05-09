import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from pwdlib import PasswordHash

from settings.jwt import settings as jwt_settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(f"{data}{padding}")


def _sign(message: bytes) -> str:
    signature = hmac.new(
        jwt_settings.SECRET_KEY.encode("utf-8"),
        message,
        hashlib.sha256,
    ).digest()
    return _b64url_encode(signature)


def create_access_token(user_id: UUID, role: str) -> tuple[str, str, int]:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=jwt_settings.ACCESS_TOKEN_LIFETIME_SECONDS)
    jti = str(uuid4())
    header = {"alg": jwt_settings.ALGORITHM, "typ": "JWT"}
    payload = {
        "sub": str(user_id),
        "jti": jti,
        "role": role,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    header_segment = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_segment = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_segment}.{payload_segment}".encode("utf-8")
    signature_segment = _sign(signing_input)
    return f"{header_segment}.{payload_segment}.{signature_segment}", jti, jwt_settings.ACCESS_TOKEN_LIFETIME_SECONDS


def decode_access_token(token: str) -> dict:
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:
        raise ValueError("Invalid token format") from exc

    signing_input = f"{header_segment}.{payload_segment}".encode("utf-8")
    expected_signature = _sign(signing_input)
    if not hmac.compare_digest(signature_segment, expected_signature):
        raise ValueError("Invalid token signature")

    payload = json.loads(_b64url_decode(payload_segment))
    now_ts = int(datetime.now(timezone.utc).timestamp())
    if payload.get("type") != "access":
        raise ValueError("Invalid token type")
    if payload.get("exp", 0) < now_ts:
        raise ValueError("Token expired")
    return payload


def build_access_token_redis_key(jti: str) -> str:
    return f"access_token:{jti}"


def create_refresh_token() -> str:
    return secrets.token_urlsafe(48)
