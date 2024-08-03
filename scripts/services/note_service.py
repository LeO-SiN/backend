from fastapi import Depends, HTTPException
from fastapi import APIRouter, status
from scripts.core.handlers.notes_handler import NotesHandler
from scripts.schemas.notes_schema import NotesSchema
from scripts.constants.api_endpoints import APIEndpoints
from scripts.schemas.user_schemas import DefaultResponse
from scripts.utils.security.jwt_util import JWT

notes_router = APIRouter(prefix=APIEndpoints.notes)

jwt = JWT()


@notes_router.get(APIEndpoints.find_notes, status_code=status.HTTP_200_OK)
def find_notes(user_data=Depends(jwt.get_current_user)):
    try:
        notes_handler = NotesHandler()
        response = notes_handler.find_notes(user_id=user_data["user_id"])
        return DefaultResponse(
            status="Success", message="Found All notes Available", data=response
        )
    except Exception as e:
        print(e.args)
        return DefaultResponse(message="Error Occured")


@notes_router.get(APIEndpoints.find_note + "/{id}", status_code=status.HTTP_200_OK)
def get_note_by_id(id: str, user_data=Depends(jwt.get_current_user)):
    try:

        notes_handler = NotesHandler()
        response = notes_handler.find_one(id=id, user_id=user_data["user_id"])
        if response:
            return DefaultResponse(
                status="Success", message=f"Found Note with ID: {id}", data=response
            )
        else:
            return DefaultResponse(message=f"Couldn't find a note with ID {id}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)


@notes_router.post(
    APIEndpoints.create_note,
    status_code=status.HTTP_201_CREATED,
)
def create_note(note: NotesSchema, user_data=Depends(jwt.get_current_user)):
    try:
        notes_handler = NotesHandler()
        note = notes_handler.create_one(data=note.dict(), user_id=user_data["user_id"])
        return note
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args
        )


@notes_router.put(APIEndpoints.update_note + "/{id}", status_code=status.HTTP_200_OK)
def update_note(id: str, note: NotesSchema, user_data=Depends(jwt.get_current_user)):
    try:
        notes_handler = NotesHandler()
        notes_handler.update_one(user_id=user_data["user_id"], id=id, data=note.dict())
        return DefaultResponse(
            status="Success", message="Successfully updated note", data=note
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args
        )


@notes_router.delete(APIEndpoints.delete_note + "/{id}", status_code=status.HTTP_200_OK)
def delete_note(id: str, user_data=Depends(jwt.get_current_user)):
    try:
        notes_handler = NotesHandler()
        notes_handler.delete_one(id=id, user_id=user_data["user_id"])
        return DefaultResponse(
            status="Success", message=f"Successfully deleted note with {id}"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)
