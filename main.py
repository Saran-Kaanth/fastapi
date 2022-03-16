from webbrowser import get
from fastapi import FastAPI,Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app=FastAPI()

class User(BaseModel):
    username:str
    email:str|None=None
    full_name:str|None=None
    disabled:bool|None=None

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")
# @app.get("/")
# async def root():
#     return {"message":"hello world!"}

@app.get("/items/")
async def read_items(token:str=Depends(oauth2_scheme)):
    return {"token":token}

def fake_decode_token(token):
    return User(
        username="saran"+"fakedecoded",email="saran@gmail.com",full_name="saran kaanth"
    )

async def get_current_user(token:str=Depends(oauth2_scheme)):
    user=fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user:User=Depends(get_current_user)):
    return current_user