# 이 파일은 uvicorn server를 시작할 코드를 담고있음/request 와 response를 asynchronously하게 하는 하는 부분 담당
#fastapi 사용할 예정

import uvicorn
from fastapi import FastAPI, Path, Request
from fastapi.responses import JSONResponse
import pandas as pd
from models import Company, Index

import workflow_runner
from models import MyException, Configuration, Index

#fastAPI 인스턴스 생성
app=FastAPI(title='SMART Science Application',description='A Smart Data Science Application running on FastAPi + uvicorn',version = '0.0.1')
#change
#index를 get해서(required!) 
@app.get("/{index}")
async def get_result(index: Index = Path(..., title="The name of the Index")
                     ):
   
    config = Configuration(
        index=index
    )
    #models.py에 있는 Configuration class를 활용
    try:
        result = await workflow_runner.run(config) #config 안에서 url 갖고옴(각 index에 맞는!)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise MyException(e) #없는 경우 다우!

#get_result는 asynchronous function
@app.exception_handler(MyException)
async def unicorn_exception_handler(request: Request, exc: MyException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Error occurred! Please contact the system admin."},
    )