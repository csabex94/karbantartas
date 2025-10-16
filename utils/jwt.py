import threading
import time
import base64
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from ..models.user import User
from ..models.jwt import JwtModel
from ..utils.exception_handler import CustomExceptionHandler


class Jwt:
    __instance = None
    __lock = threading.Lock()
    __header: dict  = {}

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = cls()
        return cls.__instance
    
    @classmethod
    def set_keys(cls, private_key: str):
        cls.__header = json.dumps({"typ": "JWT", "alg": "RS256"}).encode()
        verifier = RSA.importKey(private_key)
        cls.__verifier = PKCS1_v1_5.new(rsa_key=verifier)

    @classmethod
    def generate_token(cls, user: dict) -> str:
        now = time.time_ns()
        payload = JwtModel(
            iat=now,
            exp=now + (7 * 24 * 60 * 60),
            sub="96e67563-dd57-511c-86cd-d609655661f3",
            aud="http://localhost:8000",
            iss="http://localhost:8000",
            scope="karbantarto,karbantarto.read,karbantarto_write",
            user=User(**user)
        ).model_dump_json().encode()

        data = f"{base64.urlsafe_b64encode(cls.__header).decode()}.{base64.urlsafe_b64encode(payload).decode()}"
        digest = SHA256.new()
        digest.update(data.encode())
        signature = cls.__verifier.sign(digest)
        signature = base64.urlsafe_b64encode(signature)
        token = data + '.' + signature.decode()
        return token
    

    @classmethod
    def verify_token(cls, token: str) -> JwtModel:
        digest = SHA256.new()
        chunks = token.split('.')
        if len(chunks) != 3:
            raise CustomExceptionHandler("invalid_access_token", "Invalid number of segments.", 422)
        [header, payload, signature] = chunks
        digest.update(f"{header}.{payload}".encode())
        signature = base64.urlsafe_b64decode(signature)
        valid = cls.__verifier.verify(digest, signature)
        if valid is False:
            raise CustomExceptionHandler("invalid_access_token", "Invalid access token. Please provide a valid token.", 422)
        jwt_model = JwtModel(**json.loads(base64.urlsafe_b64decode(payload).decode()))
        return jwt_model


def init_jwt(private_key: str):
    instance = Jwt.get_instance()
    instance.set_keys(private_key)