from pydantic import EmailStr
from scripts.db.mongo.users.collections.users import Users
from scripts.db.mongo import mongo_client
from scripts.utils.security.jwt_util import JWT
from scripts.utils.security.hash import verifyPass

class LoginHandler:
    def __init__(self) -> None:
        self.users = Users(mongo_client=mongo_client)

    def validate_user(self, cred: dict):
        try:
            res = self.users.find_user(cred["email"])
            if res:
                if cred["email"] == res["email"] and verifyPass(
                    cred["password"], res["password"]
                ):

                    return (True,res["email"],res["user_id"])
                else:
                    return (False,None)
            else:
                return (False,None)

        except Exception as e:
            print(e.args)

    def create_jwt_token(self, cred: dict):
        try:
            return JWT().create_token(cred)
        except Exception as e:
            print(e.args)


    def check_new_user(self, email: EmailStr):
        try:
            ret = self.users.find_user(email=email)
            if ret == None:
                return False
            return True

        except Exception as e:
            print(e.args)
            raise