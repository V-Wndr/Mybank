from dao import db
from .models import User

def getUser(user_id: str) -> User:
    try:
        print(f'get user: {db.session.get(User, user_id)}')
        return db.session.get(User, user_id)
    except Exception as e:
        db.session.rollback()
        raise Exception(f'Error raised when creating user: {e}')

def createUser():
    """
    when user sign up, they need to provide their personal information,
    the system will create a user_key for each user, which will be used
    in user's data encryption
    """
    pass
