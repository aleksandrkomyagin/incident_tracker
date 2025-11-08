from functools import lru_cache

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key

from incident_tracker.interfaces.crypto import IRSAKeyManager


class RSAKeyManager(IRSAKeyManager):
    def generate_key(self) -> str:
        """Создаём новую пару RSA и возвращаем приватный ключ в PEM"""
        private_key = generate_private_key(public_exponent=65537, key_size=2048)
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pem.decode("utf-8")

    def get_public_key(self, private_pem: str) -> str:
        private_key = serialization.load_pem_private_key(
            private_pem.encode("utf-8"),
            password=None,
        )
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return public_pem.decode("utf-8")


@lru_cache
def get_rsa_key_generator() -> RSAKeyManager:
    return RSAKeyManager()
