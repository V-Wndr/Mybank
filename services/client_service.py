import hmac
from dao.user_dao import getUser
from user_service import UserService
from utils.crypto_utils import add_salt
import os


class ClientService:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.client = getUser(user_id=client_id)
        self.user_service = UserService(user_id=client_id)
        # Get key from environment variable
        self.master_key = 0
        # self.master_key = os.environ.get('AES_KEY').encode()
        self.is_exit = True if self.client else False

    def handle_login(self, password):
        if self.is_exit:
            return self.user_service.password_authenticate(password)
        else:
            print(f'client not exist')
            return False


