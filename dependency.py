from fastapi import FastAPI,Depends, Cookie,Header
from fastapi.exceptions import HTTPException


app=FastAPI()

class QueryParam:
    def __init__(self,name:str,age:int|None=24,q:str|None=None):
        self.name=name
        self.age=age
        self.q=q

async def query_parameters(q:str|None=None,skip:int=0,limit:int=100):
    return {"q":q,"skip":skip,"limit":limit}

@app.get("/items/",tags=["items"])
async def get_items(commons:query_parameters=Depends()):
    return commons

@app.get("/users/",tags=["users"])
# async def get_users(commons:dict=Depends(query_parameters)):
async def get_users(commons:QueryParam=Depends()):
    return commons

def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: str | None = Cookie(None)
):
    if not q:
        return last_query
    return q


@app.get("/items_1/",tags=["items"])
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items_except/", dependencies=[Depends(verify_token), Depends(verify_key)],tags=["items"],)
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

# class MySuperContextManager:
#     def __init__(self):
#         self.db = DBSession()

#     def __enter__(self):
#         return self.db

#     def __exit__(self, exc_type, exc_value, traceback):
#         self.db.close()


# async def get_db():
#     with MySuperContextManager() as db:
#         yield db