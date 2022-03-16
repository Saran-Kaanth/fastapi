from datetime import date, datetime,time,timedelta
from time import timezone
from turtle import st
from urllib.request import Request
from uuid import UUID
from fastapi import (
    Body, Cookie, FastAPI, 
    Query,Path,Header,status,
    Form,File,UploadFile,
    HTTPException
)
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)
from enum import Enum
from pydantic import BaseModel,Field,HttpUrl,EmailStr
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse,JSONResponse,PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

class UnicornException(Exception):
    def __init__(self,name:str,age:int|None=Query(23)):
        self.name=name
        self.age=age

app=FastAPI()


class Color(Enum):
    red="1"
    blue="2"
    green="3.05"
    white=True

user_data=[{"id":1,"name":"saran"},{"id":2,"name":"sam"},{"id":3,"name":"logiya"}]
item_data=[{"id":1,"name":"milk"},{"id":2,"name":"bread"},{"id":3,"name":"butter"}]
fake_items_db=[{"item":"milk"},{"item":"butter"},"bread",{"item_no":3}]
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


class Image(BaseModel):
    url:HttpUrl
    name:str

class Item_2(BaseModel):
    name:str|None=Field(None,title="Name of the item")
    desc:str|None=None
    price:float
    tax:float|None=None
    tags:list[str]=[]

#Nested models
class Item(BaseModel):
    name:str|None=Field(None,title="Name of the item")
    desc:str|None=None
    price:float
    tax:float|None=None
    # tags:set[str]=set()

    class Config:
        schema_extra={
            "example":{
                "name":"milk",
                "desc":"item name",
                "price":3.05,
                "tax":34.5
            }
        }
    # image:list[Image]|None=None
    # sell_date:date|None=None

class Offer(BaseModel):
    name:str
    price:float|None=None
    item:list[Item]|None=None

class User(BaseModel):
    name:str
    age:int

class UserBase(BaseModel):
    name:str
    email:EmailStr
    age:int|None=None

class UserIn(UserBase):
    # name:str
    password:str=Field(...,min_length=8,max_length=24)
    # email:EmailStr
    # age:int

class UserOut(UserBase):
    pass
    # name:str
    # email:EmailStr
    # age:int
class UserInDB(UserBase):
    hashed_password:str

def fake_password_hasher(password:str):
    return "hasher"+password+"dfkjdfnj"

def fake_password_db(user_in:UserIn):
    hashed_password=fake_password_hasher(user_in.password)
    print(hashed_password)
    UserDB=UserInDB(**user_in.dict(),hashed_password=hashed_password)
    return UserDB

@app.post("/store_user",response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def post_user(user_in:UserIn):
    user_saved=fake_password_db(user_in)
    return user_saved

items_1 = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.patch("/patch_item/{item_id}",response_model=Item_2)
async def patch_item(item_id:str,item:Item):
    stored_item_data=items_1[item_id]
    print(stored_item_data)
    stored_item_model=Item_2(**stored_item_data)
    print(stored_item_model)
    updated_data=item.dict(exclude_unset=True)
    print(updated_data)
    updated_item=stored_item_model.copy(update=updated_data)
    print(updated_item)
    items_1[item_id]=jsonable_encoder(updated_item)
    return updated_item
    # print(updated_data)
    # return "hii"

@app.put("/items_put/{item_id}", response_model=Item,tags=["items"])
async def update_item(item_id: str, item: Item):
    print(items_1[item_id])
    update_item_encoded = jsonable_encoder(item)
    print(update_item_encoded)
    items_1[item_id] = update_item_encoded
    print(items_1[item_id])
    return update_item_encoded

#handling errors
items = {"foo": "The Foo Wrestlers"}


@app.get("/items-header/{item_id}",tags=["items"],
            summary="Create an item",
            description="Create an item with all the information, name, description, price, tax and a set of unique tags")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


@app.exception_handler(UnicornException)
async def unicorn_handler(request:Request,exc:UnicornException):
    print(exc)
    return JSONResponse(
        status_code=418,
        content={"message":f"{exc.name} the name {exc.age} is the age" }
    )

@app.get("/unicorn/{name}")
async def unicorn(name:str,age:int|None=None):
    if name!="ndnfkjnf":
        raise UnicornException(name=name,age=age)
    return {"name":name}

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return JSONResponse(str(exc), status_code=400)

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.get("/items_error/{item_id}",tags=["items"])
async def read_item_1(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Item_1(BaseModel):
    title: str
    size: int


@app.post("/items/",tags=["items"])
async def create_item(item: Item_1):
    return item

#forms and files
@app.post("/form_files/",tags=["files"])
async def form_and_files(file_2:UploadFile=File(...),file_1:bytes=File(...),token:str=Form(...)):
    return {
        "file_1":len(file_1),
        "file_type":file_2.content_type,
        "file_name":file_2.filename,
        "token":token
    }

#files
@app.post("/files/",tags=["files"])
async def create_files(
    files: list[bytes] = File(..., description="Multiple files as bytes")
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/",tags=["files"])
async def create_upload_files(
    files: list[UploadFile] = File(..., description="Multiple files as UploadFile")
):
    print(file.read for file in files)
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

#form data
@app.post("/login/",tags=["users"])
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


#response model
@app.get("/get_items/{item_id}",response_model=Item,tags=["items"],response_model_exclude_unset=True)
async def get_item_model(item_id:str):
    return items[item_id]

@app.post("/get_users",response_model=UserOut,tags=["users"])
async def get_user_model(user:UserIn):
    return user


#header parameters
@app.get("/get_headers")
async def get_headers(strange_header:str|None=Header(None,convert_underscores=False),
                      x_tokens:list[str]|None=Header(None)):
    return {"strange":strange_header,"X_tokens":x_tokens}

#cookie parameters
@app.get("/get_cookies")
async def get_cookies(cookie_id:str|None=Cookie(...)):
    print(cookie_id)
    return {"cookie_id":cookie_id}

#extra data types
@app.put("/new_item",tags=["items"])
async def put_new_item(*,
                       item_id:UUID|None="13jhb4b",
                       order_date:datetime|None=datetime.now(),
                       deli_date:datetime|None=Body(None),
                       duration:timedelta|None=None):
    total_time=deli_date-order_date
    return {"item_id":item_id,
            "order_date":order_date,
            "deli_date":deli_date,
            "duration":duration,
            "total_time":total_time}

#decalre request example data
@app.put("/items/{item_id}",tags=["items"])
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

#Body Fields
@app.post("/offers/",tags=["items"])
async def create_offer(offer: Offer):
    return offer

# Body Parameters
@app.put("/put_user/{user_id}",tags=["users"])
async def update_item(*,item_id:int,
                      item:Item,
                      user:User,
                      importance:int=Body(...,gt=3),
                      q:str|None=Query(...,min_length=3,max_length=5)):
    results={"item_id":item_id,"item":item,"user":user,"importance":importance}
    if q:
        results.update({"q":q})
        return results
    return results

@app.put("/put_item/{item_id}",tags=["items"])
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


# Query Parameters
@app.get("/users/",tags=["users"])
async def get_user(user_ids:list[str]|None=Query(...,min_length=2,max_length=4,
                                        alias="user id's",description="getting user credentials",deprecated=False)):
    print(user_ids)
    return user_ids

# path parameters
@app.get('/items/{item_id}',tags=["items"])
async def get_item_path(item_id:int=Path(...,title="Enter item id"),price:float|None=Query(...,le=20.8,ge=3.5)):
    for item in item_data:
        if item["id"]==item_id:
            item_name=item["name"]
    
    if item_name:
        return {"item_id":item_id,"name":item_name,"price":price}
    return "No item found"


@app.post("/items",tags=["items"])
async def price_tax(item:Item,item_id:int|None=None):
    print(Item)
    print(item)
    print(item.dict())
    items=item.dict()
    if item_id:
        items.update({"item_id":item_id})
        return {"items":item_id,**item.dict()}
    return item.dict()



@app.get('/user_id/{user_id}/item_id/{item_id}',tags=["items","users"])
async def get_user(user_id:int,item_id:int,q:str|None=None,v:bool=False):
    item_name=None
    user_name=None
    for user in user_data:
        if user["id"]==user_id:
            user_name=user["name"]
    for item in item_data:
        if item["id"]==item_id:
            item_name=item["name"]
            # return {"user_name":user["name"]}
    if user_name==None or item_name==None:
        return {"message":"No user found"}
    else:
        out_val={"user_name":user_name,"item_name":item_name}
        if q and not v:
            out_val.update({"q":q})
            return out_val
        elif v and not q:
            out_val.update({"v":v})
            return out_val
        elif q and v:
            out_val.update({"q":q,"v":v})
            return out_val
        return out_val
            


@app.get('/items_1/{item_id}',tags=["items"])
async def read_item(item_id:int,q:str|None=None,v:bool=None):
    print(item_id)
    if q or v:
        return {"item":item_id,"q":q,"v":v}
    return {"item":item_id}
async def read_item(skip:int=0,limit:int=4):
    print(skip+limit)
    print(fake_items_db[skip:skip+limit])
    return fake_items_db[skip:limit]

@app.get('/items/{item_id}',tags=["items"])
async def root(item_id:bool):
    print(item_id)
    return {"name":item_id}

@app.get('/colors/{color_name}')
async def root(color_value:Color):
    print(color_value)
    print(Color)
    return {"color_value":color_value.name}

@app.get("/read_file/{file_path:path}",tags=["files"])
async def get_file(file_path:str):
    return {"file_path":file_path}