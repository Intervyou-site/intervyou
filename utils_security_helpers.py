# utils_security_helpers.py
"""
Simple security helpers:
- bcrypt password hashing/verification using passlib
- safe file saving helpers (sync + async limited)
"""

from passlib.context import CryptContext
import uuid
from pathlib import Path
from typing import Union
from fastapi import UploadFile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a plaintext password (bcrypt)."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def save_upload_sync(upload_file: UploadFile, dest_dir: str) -> str:
    """
    Save an UploadFile (synchronous) to dest_dir with a UUID filename.
    Returns the saved filepath as a string.
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    ext = Path(upload_file.filename).suffix or ""
    filename = f"{uuid.uuid4().hex}{ext}"
    out_path = dest / filename

    # UploadFile.file is a file-like object - read its bytes
    data = upload_file.file.read()
    with out_path.open("wb") as f:
        f.write(data)
    return str(out_path)


async def save_upload_limited(upload_file: UploadFile, dest_dir: str, max_bytes: int = 10 * 1024 * 1024) -> str:
    """
    Async-save chunks from UploadFile with an enforced size limit (default 10MB).
    Use this in endpoints declared async.
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    ext = Path(upload_file.filename).suffix or ""
    filename = f"{uuid.uuid4().hex}{ext}"
    out_path = dest / filename

    total = 0
    with out_path.open("wb") as f:
        while True:
            chunk = await upload_file.read(1024 * 1024)  # read up to 1MB chunks
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                # remove partial file and raise
                try:
                    out_path.unlink(missing_ok=True)
                except Exception:
                    pass
                raise ValueError("File too large")
            f.write(chunk)
    return str(out_path)
