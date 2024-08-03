from typing import Dict, Optional
from pymongo.cursor import Cursor
from pymongo import MongoClient


class MongoConnect:
    def __init__(self, uri):
        try:
            self.uri = uri
            self.client = MongoClient(self.uri, connect=False)

        except Exception:
            raise

    def __call__(self, *args, **kwds):
        return self.client


class MongoCollectionBaseClass:
    def __init__(self, mongo_client, database, collection):
        self.client = mongo_client
        self.database = database
        self.collection = collection
        self.__database = None

    def insert_one(self, data: dict):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.insert_one(data)

        except Exception as e:
            raise

    def find(
        self,
        query: Dict,
        filter_dict: Optional[Dict] = None,
        sort=None,
        skip: Optional[int] = 0,
        limit: Optional[int] = None,
    ) -> Cursor:
        if sort == None:
            sort = list()
        if filter_dict == None:
            filter_dict = {"_id": 0}
        database_name = self.database
        collection_name = self.collection
        try:
            db = self.client[database_name]
            collection = db[collection_name]
            if len(sort) > 0:
                cursor = (
                    collection.find(
                        query,
                        filter_dict,
                    )
                    .sort(sort)
                    .skip(skip)
                )
            else:
                cursor = collection.find(query, filter_dict).skip(skip)
            if limit:
                cursor = cursor.limit(limit)

            return cursor
        except Exception as e:
            raise

    def find_one(self, query: Dict, filter_dict: Optional[Dict] = None):
        try:
            database_name = self.database
            collection_name = self.collection
            if filter_dict == None:
                filter_dict = {"_id": 0}
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.find_one(query, filter_dict)
            return response
        except Exception as e:
            raise

    def update_one(self, query: Dict, data: Dict, upsert: bool):
        try:

            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.update_one(query, {"$set": data}, upsert=upsert)
            return response.modified_count
        except Exception as e:
            raise

    def delete_one(self, query: Dict):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.delete_one(query)
            return response.deleted_count
        except Exception as e:
            raise

    def update_push_array(
        self, query: Dict, data: str, array_key: str, upsert: bool = True
    ):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.update_one(
                query, {"$push": {array_key: data}}, upsert=upsert
            )
            return response.modified_count

        except Exception as e:
            raise

    def update_pull_array(
        self, query: Dict, data: str, array_key: str, upsert: bool = True
    ):
        try:
            database_name = self.database
            collection_name = self.collection
            db = self.client[database_name]
            collection = db[collection_name]
            response = collection.update_one(
                query, {"$pull": {array_key: data}}, upsert=upsert
            )
            return response.modified_count

        except Exception as e:
            print(e.args)
            raise
