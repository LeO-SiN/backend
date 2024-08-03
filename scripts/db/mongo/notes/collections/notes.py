from typing import Optional
from scripts.constants import CollectionNames, DatabasesNames
from scripts.db.mongo.schema import MongoBaseSchema
from scripts.utils.mongo_util import MongoCollectionBaseClass


class NoteSchema(MongoBaseSchema):
    title: str
    description: str
    tag: str

class Notes(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(
            mongo_client=mongo_client,
            database=DatabasesNames.notebook,
            collection=CollectionNames.notes,
        )

    def find_all_notes(self, user_id: str):
        notes = self.find(query={"user_id": user_id})
        if notes:
            return list(notes)

    def find_note(self, user_id, note_id):
        note = self.find_one(query={"user_id": user_id, "note_id": note_id})
        if note:
            return note

    def create_note(self, data: dict):
        self.insert_one(data=data)
    
    def update_note(self,user_id,note_id,data:dict):
        self.update_one(query={"user_id":user_id, "note_id":note_id}, data=data, upsert=False)
    
    def delete_note(self,user_id,note_id):
        self.delete_one(query={"user_id":user_id, "note_id":note_id})