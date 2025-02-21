from .models import Role, User, UserKey
from utils.crypto_utils import add_salt, generate_salt, encrypt_data, generate_key, master_key


def init_demo_data(db):
    print('create demo data, including Role(admin, client, employee), 3 Users (admin1, client1, employee 1， )')
    
    # 检查是否已经初始化（通过检查admin角色是否存在）
    if not db.session.query(Role).filter_by(name="admin").first():
        try:

            # 创建角色
            roles = {
                "admin": Role(
                    name="admin",
                    description="System Administrator",
                ),
                "employee": Role(
                    name="employee",
                    description="Bank Employee",
                ),
                "client": Role(
                    name="client",
                    description="Client",
                )
            }
            
            # 添加角色到数据库
            for role in roles.values():
                db.session.add(role)
            db.session.commit()

            # 创建示例用户
            for user_data in [
                ("admin", "Administrator", "admin@bank.com", "admin", 1),
                ("employee", "Employee", "employee@bank.com", "employee", 2),
                ("client", "Client", "client@bank.com", "client", 3)
            ]:
                username, name, email, phone, role_id = user_data
                salt = generate_salt()
                aes_key = generate_key()
                user = User(
                    role_id=role_id,
                    encrypted_name=encrypt_data(name, aes_key),
                    salt=salt,
                    encrypted_email=encrypt_data(email, aes_key),
                    encrypted_phone=encrypt_data(phone, aes_key),
                    encrypted_address=encrypt_data("demo address", aes_key),
                    encrypted_balance=encrypt_data("1000.00", aes_key),
                    password_hash=add_salt(key='123456', salt=salt),
                    is_active=True
                )
                db.session.add(user)
                print(f'db add user: {user.id}, role: {role_id}')

                # 存储用户的AES密钥到表aes_key中
                user_key = UserKey(user_id=user.id, encrypted_key=encrypt_data(master_key, aes_key))
                db.session.add(user_key)
            db.session.commit()


        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error initializing demo data: {e}")
