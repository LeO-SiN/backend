from scripts.db.mongo.users.collections.users import Users
from scripts.db.mongo import mongo_client
from scripts.utils.security.hash import hashPassword
import string
import random

class UserHandler:
    def __init__(self):
        self.users = Users(mongo_client=mongo_client)

    def find_users(self):
        try:
            return self.users.find_all_users()
        except Exception as e:
            print(e.args)
            return None

    def find_one(self, email):
        try:
            return self.users.find_user(email)
        except Exception as e:
            print(e.args)
            return None

    def create_one(self, data: dict):
        try:
            data["password"] = hashPassword(data["password"])
            data["user_id"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            self.users.create_user(data=dict(data))
            return True
        except Exception as e:
            print(e.args)

    def update_one(self, user_id: str, data: dict):
        try:
            data["password"] = hashPassword(data["password"])
            self.users.update_user(user_id=user_id, data=dict(data))
        except Exception as e:
            print(e.args)

    def delete_one(self, eid: str):
        try:
            self.users.delete_user(eid=eid)
        except Exception as e:
            print(e.args)
