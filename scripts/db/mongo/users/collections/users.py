from pydantic import EmailStr
from scripts.constants import DatabasesNames, CollectionNames
from scripts.db.mongo.schema import MongoBaseSchema
from scripts.utils.mongo_util import MongoCollectionBaseClass


class UsersSchema(MongoBaseSchema):
    name: str
    email: EmailStr
    password: str
    user_id: str


class Users(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(
            mongo_client=mongo_client,
            database=DatabasesNames.notebook,
            collection=CollectionNames.users,
        )

    def find_all_users(self):
        users = self.find(query={})
        if users:
            return list(users)

    def find_user(self, email):
        user = self.find_one(query={"email": email})
        if user:
            return user

    def create_user(self, data: dict):
        self.insert_one(data=data)

    def update_user(self, user_id: str, data: dict):
        self.update_one(query={"user_id": user_id}, data=data, upsert=True)

    def delete_user(self, user_id: str):
        self.delete_one(query={"user_id": user_id})
