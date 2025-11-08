from abc import abstractmethod
from typing import Protocol


class IRSAKeyManager(Protocol):
    @abstractmethod
    def generate_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_public_key(self, private_pem: str) -> str:
        raise NotImplementedError
