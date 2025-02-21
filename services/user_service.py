import hmac
from utils.crypto_utils import master_key, add_salt
from dao.user_dao import getUser

"""处理用户共有的逻辑"""

class UserService():
    def __init__(self, user_id: str):
        self.user_id = user_id
    def password_authenticate(self, password: str) -> bool:
        """authenticate client with password, use hash(SHA256)"""
        target = getUser(self.user_id)
        # hash gained password with SHA256 and salt
        salt = target.salt
        hashed_password = add_salt(password, salt)
        target_hashed_password = target.password_hash
        print(f"user's salt: {salt}\npassword_hash: {hashed_password}\ndb_password_hash:{target_hashed_password}")
        # compare with target password using to avoid timing attack
        if hmac.compare_digest(hashed_password, target_hashed_password):
            print("password authenticated")
            return True
        print("password not authenticated")
        return False
