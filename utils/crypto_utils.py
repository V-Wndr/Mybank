import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from dao.models import User
from cryptography.hazmat.primitives import padding


master_key = os.getenv('MASTER_KEY')
print(f'get master_key: {master_key}')

def generate_salt() -> bytes:
    """uniform salt as 16 bytes"""
    return os.urandom(16)

def add_salt(key: str, salt: bytes) -> bytes:
    argon2id = Argon2id(
        salt=salt,
        length=32,
        memory_cost=8192,
        lanes=1,
        iterations=2
    )
    password_hash = argon2id.derive(key.encode())
    return password_hash

def generate_key() -> bytes:
    """Generate a 256-bit key for encryption"""
    return os.urandom(32)

def encrypt_data(msg: any, key: bytes) -> bytes:
    """Encrypt data using a key of length 32 bytes"""
    # 生成随机IV，长度为16
    iv = os.urandom(16)
    
    # 创建加密器
    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    ).encryptor()
    
    # 将消息转换为字节并添加填充
    padder = padding.PKCS7(128).padder()
    msg_bytes = str(msg).encode()
    padded_data = padder.update(msg_bytes) + padder.finalize()
    
    # 加密数据
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    
    # 返回IV和密文的组合
    return iv + cipher_text

def decrypt_data(cipher_text: bytes, key: bytes) -> str:
    # 提取IV和密文
    iv = cipher_text[:16]
    cipher_text = cipher_text[16:]

    # 创建解密器
    decryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    ).decryptor()

    # 解密数据
    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
    
    # 去除填充
    unpadder = padding.PKCS7(128).unpadder()
    return (unpadder.update(decrypted_data) + unpadder.finalize()).decode()
    


def update_master_key(self, new_master_key: str):
    """
    Update the master_key, store it in the environment variable,
    and update the encryption keys for all users
    """
    self.master_key = new_master_key.encode()
    for user in User.select_for_update():
        pass



