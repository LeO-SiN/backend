from fastapi import Depends, HTTPException
from fastapi import APIRouter, status
from scripts.constants.api_endpoints import APIEndpoints
from scripts.core.handlers.user_handler import UserHandler
from scripts.schemas.user_schemas import DefaultResponse, UserRequestSchema, ResponseModel
from scripts.utils.security.jwt_util import JWT

users_router = APIRouter(prefix=APIEndpoints.users)


@users_router.get(APIEndpoints.find_users, status_code=status.HTTP_200_OK)
def find_users(user_id: str = Depends(JWT().get_current_user)):
    try:
        
        user_handler = UserHandler()
        response = user_handler.find_users()
        return DefaultResponse(
            status="Success", message="Found All users Available", data=response
        )
    except Exception as e:
        print(e.args)
        return DefaultResponse(message="Error Occured")


@users_router.get(APIEndpoints.find_user + "/{id}", status_code=status.HTTP_200_OK)
def get_user_by_id(id: str,user_id: str = Depends(JWT().get_current_user)):
    try:
       
        user_handler = UserHandler()
        response = user_handler.find_one(eid=id)
        if response:
            return DefaultResponse(
                status="Success", message=f"Found User with ID: {id}", data=response
            )
        else:
            return DefaultResponse(message=f"Couldn't find a user with ID {id}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)


@users_router.post(APIEndpoints.add_user, status_code=status.HTTP_201_CREATED,response_model=ResponseModel)
def create_user(user: UserRequestSchema,user_id: str = Depends(JWT().get_current_user)):
    try:
        user_handler = UserHandler()
        user_handler.create_one(data=user.dict())
        return user
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args
        )


@users_router.put(APIEndpoints.update_user, status_code=status.HTTP_200_OK)
def update_user(user: UserRequestSchema):
    try:
        user_handler = UserHandler()
        user_handler.update_one(eid=user.eid, data=user.dict())
        return DefaultResponse(
            status="Success", message="Successfully updated user", data=user
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args
        )


@users_router.delete(APIEndpoints.remove_user + "/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: str):
    try:
        user_handler = UserHandler()
        user_handler.delete_one(eid=id)
        return DefaultResponse(
            status="Success", message=f"Successfully deleted user with {id}"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)
