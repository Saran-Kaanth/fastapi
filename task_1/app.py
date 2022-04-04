import pandas as pd
from fastapi import FastAPI,status
from fastapi.responses import JSONResponse,Response

app=FastAPI()

@app.get('/get_skill',tags=["skillset"])
async def get_skill_by_name(emp_name:str):
    df=pd.read_csv("mcv_data_test.txt",skiprows=[0,2],sep='|')
    df=df.loc[:,~df.columns.str.contains('^Unnamed')]
    df.columns=df.columns.str.strip()
    skillset=[]
    for i,row in df.iterrows():
        if row.EmployeeName.strip().lower()==emp_name.lower():
            skillset.append(row.SkillName.strip())
    if(len(skillset)!=0):
        return JSONResponse(content={"skillsets":skillset},status_code=status.HTTP_200_OK)
    return JSONResponse(content="User Not Found",status_code=status.HTTP_404_NOT_FOUND)
    
