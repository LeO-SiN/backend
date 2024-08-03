from fastapi import APIRouter, Depends, HTTPException, status
from scripts.core.handlers.login_handler import LoginHandler
from scripts.core.handlers.user_handler import UserHandler
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from scripts.schemas.user_schemas import UserRequestSchema

user_cred = APIRouter()


@user_cred.post("/login")
def login(cred: OAuth2PasswordRequestForm = Depends()):
    try:
        login_handler = LoginHandler()
        response, email, user_id = login_handler.validate_user(
            {"email": cred.username, "password": cred.password}
        )
        if response:

            return {
                "detail": {"success": True,
                "access_token": login_handler.create_jwt_token(
                    {"email": cred.username, "user_id": user_id}
                ),
                "token_type": "bearer"}
            }
        else:
            raise Exception
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "detail": "Incorrect Username or Password"},
        )


@user_cred.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_det: UserRequestSchema):
    try:
        login_handler = LoginHandler()
        if not login_handler.check_new_user(user_det.dict()["email"]):
            user_handler = UserHandler()
            ret = user_handler.create_one(user_det.dict())
            if ret:
                return {
                    "status": True,
                    "name": user_det.name,
                    "email": user_det.email,
                }
            else:
                raise
        else:
            raise

    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="email already existing",
        )
