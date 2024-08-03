from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from scripts.services.user_service import users_router
from scripts.services.login_service import user_cred
from scripts.services.note_service import notes_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(users_router)
app.include_router(user_cred)
app.include_router(notes_router,tags=["Notes"])
