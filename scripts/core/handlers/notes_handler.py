from datetime import datetime
import string
from scripts.db.mongo.notes.collections.notes import Notes
from scripts.db.mongo import mongo_client
import random


class NotesHandler:
    def __init__(self):
        self.notes = Notes(mongo_client=mongo_client)

    def find_notes(self, user_id: str):
        try:
            return self.notes.find_all_notes(user_id)
        except Exception as e:
            print(e.args)
            return None

    def find_one(self, id: str, user_id: str):
        try:
            return self.notes.find_note(user_id=user_id, note_id=id)
        except Exception as e:
            print(e.args)
            return None

    def create_one(self, data: dict, user_id: str):
        try:
            data["note_id"] = str(user_id) +'_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            data["user_id"] = user_id
            data["created_at"] = "{}".format(datetime.now())
            self.notes.create_note(data=dict(data))
            return data
        except Exception as e:
            print(e.args)

    def update_one(self, user_id: str, id: str, data: dict):
        try:

            self.notes.update_note(user_id=user_id, note_id=id, data=dict(data))
        except Exception as e:
            print(e.args)

    def delete_one(self, id: str, user_id: str):
        try:
            self.notes.delete_note(user_id=user_id, note_id=id)
        except Exception as e:
            print(e.args)