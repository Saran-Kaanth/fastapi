from fastapi import FastAPI,Depends

app=FastAPI()

async def query_parameters(q:str|None=None,skip:int=0,limit:int=100):
    return {"q":q,"skip":skip,"limit":limit}

@app.get("/items/",tags=["items"])
async def get_items(commons:query_parameters=Depends()):
    return commons

@app.get("/users/",tags=["users"])
async def get_users(commons:dict=Depends(query_parameters)):
    return commons