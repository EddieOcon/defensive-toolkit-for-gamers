# safevault/core.py
import os
import json
import secrets
import string
from dataclasses import dataclass
from typing import Dict, Optional

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

VAULT_FILE_DEFAULT = "vault.bin"
SALT_SIZE = 16
NONCE_SIZE = 12

# scrypt params (good baseline for desktop)
SCRYPT_N = 2**15   # CPU/memory cost
SCRYPT_R = 8
SCRYPT_P = 1
KEY_LEN = 32


class VaultError(Exception):
    """Base class for vault errors."""


class VaultAuthError(VaultError):
    """Raised when the master password is wrong or vault cannot be decrypted."""


@dataclass
class VaultEntry:
    name: str
    username: str
    password: str
    notes: str = ""


class SafeVault:
    """
    Encrypted local password vault.
    - Uses scrypt KDF + AES-GCM
    - Stores everything in a single binary vault file.
    """

    def __init__(self, path: str = VAULT_FILE_DEFAULT):
        self.path = path
        self.entries: Dict[str, VaultEntry] = {}

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        kdf = Scrypt(
            salt=salt,
            length=KEY_LEN,
            n=SCRYPT_N,
            r=SCRYPT_R,
            p=SCRYPT_P
        )
        return kdf.derive(password.encode("utf-8"))

    @staticmethod
    def _encrypt(key: bytes, plaintext: bytes) -> bytes:
        aes = AESGCM(key)
        nonce = secrets.token_bytes(NONCE_SIZE)
        ct = aes.encrypt(nonce, plaintext, None)
        return nonce + ct

    @staticmethod
    def _decrypt(key: bytes, blob: bytes) -> bytes:
        aes = AESGCM(key)
        nonce = blob[:NONCE_SIZE]
        ct = blob[NONCE_SIZE:]
        return aes.decrypt(nonce, ct, None)

    def _to_dict(self) -> dict:
        return {
            "entries": {
                name: {
                    "username": e.username,
                    "password": e.password,
                    "notes": e.notes,
                }
                for name, e in self.entries.items()
            }
        }

    def _from_dict(self, data: dict):
        self.entries = {}
        for name, info in data.get("entries", {}).items():
            self.entries[name] = VaultEntry(
                name=name,
                username=info.get("username", ""),
                password=info.get("password", ""),
                notes=info.get("notes", ""),
            )

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def create_new(self, master_password: str):
        """Create an empty vault (overwrites existing file if present)."""
        self.entries = {}
        self.save(master_password)

    def load(self, master_password: str):
        """Load vault from disk and decrypt into memory."""
        if not self.exists():
            self.entries = {}
            return

        try:
            raw = open(self.path, "rb").read()
        except OSError as e:
            raise VaultError(f"Could not read vault file: {e}")

        if len(raw) < SALT_SIZE + NONCE_SIZE:
            raise VaultError("Vault file is too small / corrupted")

        salt = raw[:SALT_SIZE]
        blob = raw[SALT_SIZE:]
        try:
            key = self._derive_key(master_password, salt)
            dec = self._decrypt(key, blob)
            data = json.loads(dec.decode("utf-8"))
            self._from_dict(data)
        except Exception as e:
            raise VaultAuthError("Invalid master password or corrupted vault") from e

    def save(self, master_password: str):
        """Encrypt current entries and write vault file."""
        salt = secrets.token_bytes(SALT_SIZE)
        key = self._derive_key(master_password, salt)
        data = self._to_dict()
        plaintext = json.dumps(data, ensure_ascii=False).encode("utf-8")
        blob = self._encrypt(key, plaintext)

        try:
            with open(self.path, "wb") as fh:
                fh.write(salt + blob)
            try:
                os.chmod(self.path, 0o600)
            except Exception:
                # Best-effort on Windows
                pass
        except OSError as e:
            raise VaultError(f"Could not write vault file: {e}")

    def add_entry(self, entry: VaultEntry):
        self.entries[entry.name] = entry

    def delete_entry(self, name: str):
        self.entries.pop(name, None)

    def get_entry(self, name: str) -> Optional[VaultEntry]:
        return self.entries.get(name)

    def list_entries(self):
        return list(self.entries.values())

    @staticmethod
    def generate_password(length: int = 16) -> str:
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}"
        return "".join(secrets.choice(alphabet) for _ in range(length))
