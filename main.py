from http.client import HTTPException
from tkinter import DISABLED
from fastapi import FastAPI,Depends,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app=FastAPI()

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token_provider")

class User(BaseModel):
    username:str
    email:str|None=None
    full_name:str|None=None
    disabled:bool|None=None

class UserInDB(User):
    hashed_password:str

def get_user(db,username:str):
    if username in db:
        user_dict=db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user=get_user(fake_users_db,token),
    return user

# @app.get("/")
# async def root():
#     return {"message":"hello world!"}

# @app.get("/items/",tags=["items"])
# async def read_items(token:str=Depends(oauth2_scheme)):
#     return {"token":token}


    # return User(
    #     username="saran"+"fakedecoded",email="saran@gmail.com",full_name="saran kaanth"
    # )

async def get_current_user(token:str=Depends(oauth2_scheme)):
    user=fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )
    print(user)
    return user
    # user=fake_decode_token(token)
    # return user

async def get_current_active_user(current_user:User=Depends(get_current_user)):
    print(current_user.username)
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Inactive user")
    return current_user

@app.post("/token_provider")
async def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user_dict=fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400,detail="Check the username or password")
    user=UserInDB(**user_dict)
    hashed_password=fake_hash_password(form_data.password)
    if not hashed_password==user.hashed_password:
        raise HTTPException(status_code=400,detail="Check the username or password")
    
    return {"access_token":user.username,"token_type":"bearer"}


@app.get("/users/me")
async def read_users_me(current_user:User=Depends(get_current_active_user)):
    return current_user