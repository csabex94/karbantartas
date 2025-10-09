import threading
import secrets
import hashlib
import base64

from secret_key_generator import secret_key_generator
from keycove import hash, generate_token, encrypt, decrypt
from cryptography.fernet import Fernet



class SecurityUtils:
    __instance = None
    __lock = threading.Lock()

    CHARS_SECRET: str = "0123456789abcdefghijklmnoprstuvwxzy-_"

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = cls()
        return cls.__instance
    
    @classmethod
    def set_api_key_secret(cls, api_key_secret: str):
        cls.__api_key_secret = api_key_secret
        
    @classmethod
    def generate_api_key_token(cls) -> str:
        token: str = generate_token()
        return token
    
    @classmethod
    def protect_api_key_token(cls, token: str) -> list[str]:
        hashed: str = hash(token)
        encrypted: str = encrypt(token, cls.__api_key_secret)
        return [hashed, encrypted]
    
    @classmethod
    def decrypt_api_key(cls, value: str):
        return decrypt(value, cls.__api_key_secret)
    
    @classmethod
    def md5_hash(self, value: str) -> str:
        return hashlib.md5(value.encode('utf-8')).hexdigest()
    
    @classmethod
    def sha1_hash(self, value: str) -> str:
        return hashlib.sha1(string=value.encode('utf-8')).hexdigest()
    
    @classmethod
    def sha256_hash(self, value: str) -> str:
        return hash(value)
    
    
    @classmethod
    def device_signature_base64(cls, signature: str) -> str:
        return base64.urlsafe_b64encode(signature.encode()).decode()

    @classmethod
    def device_signature_decodeb64(cls, encoded: str) -> str:
        b64_encoded = base64.urlsafe_b64decode(encoded.encode()).decode()
        b64_encoded.replace('==', '')
        return b64_encoded

    @classmethod
    def string_to_bytes(self, val: str):
        return base64.urlsafe_b64decode(f"{val}===")

    @classmethod
    def bytes_to_string(self, val: bytes):
        return base64.urlsafe_b64encode(val).decode("utf-8").rstrip("=")
    
    
    @classmethod
    def generate_random_secret(self, lenght: int = 20) -> str:
        return secrets.token_urlsafe(lenght)
    
    @classmethod
    def generate_secret_key(self, lenght: int = 14) -> str:
        return secret_key_generator.generate(chars=self.CHARS_SECRET, len_of_secret_key=lenght)


def init_security_utils(api_key_secret: str):
    utils = SecurityUtils.get_instance()
    utils.set_api_key_secret(api_key_secret)