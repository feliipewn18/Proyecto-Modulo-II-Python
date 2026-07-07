import bcrypt
import os
from cryptography.fernet import Fernet
from typing import Union
import base64

def hash_password(pwd: str) -> str:
    bytes_pwd = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(bytes_pwd, salt)
    return hashed_pwd.decode('utf-8')

def verify_password(hashed_pwd: str, pwd: str) -> bool:
    bytes_hashed_pwd = hashed_pwd.encode('utf-8')
    bytes_pwd = pwd.encode('utf-8')
    return bcrypt.checkpw(bytes_pwd, bytes_hashed_pwd)

class CryptoHelper:
    def __init__(self):
        self._key = os.getenv('FERNET_SECRET_KEY')
        self.validate_key()
        self.fernet = Fernet(self._key)
    
    def encrypt(self, value: Union[str, int, float, bool]) -> str:
        string_value = str(value)

        bytes_value = string_value.encode('utf-8')
        encrypted_value = self.fernet.encrypt(bytes_value)
        return encrypted_value.decode('utf-8')
    
    def decrypt(self, value: str) -> Union[str, int, float, bool]:
        bytes_value = value.encode('utf-8')
        decrypted_value = self.fernet.decrypt(bytes_value)
        return decrypted_value.decode('utf-8')
    
    def validate_key(self):
        if not self._key:
            raise ValueError('FERNET_SECRET_KEY is not set')
        
        try:
            bytes_key = base64.urlsafe_b64decode(self._key)

            if len(bytes_key) != 32:
                raise ValueError('Invalid key length')
        except ValueError as e:
            raise ValueError(f'{e}')