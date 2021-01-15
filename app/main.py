import json
from pydantic import BaseModel
from fastapi import FastAPI,File, UploadFile,Form
from typing import List
from worker import celery
from PIL import Image
from tensorflow.keras import layers
from tensorflow.keras import Model
from keras.preprocessing import image
from keras.preprocessing import image
import numpy as np
from keras.models import model_from_json
import tensorflow as tf
import base64
import numpy as np
from fastapi.encoders import jsonable_encoder
import redis
from io import BytesIO, StringIO
from time import sleep
redis_store = redis.Redis.from_url("redis://redis_server:6379/10")

app=FastAPI()
class Item(BaseModel):
    name: str
class Filename(BaseModel):
    filename:str

@app.post("/task_hello_world/")
async def create_item(item: Item):
    task_name = "hello.task"
    task = celery.send_task(task_name, args=[item.name])
    return dict(id=task.id, url='localhost:5000/check_task/{}'.format(task.id))

    
@app.post("/task_bye_world/")
async def create_item_bye(img:UploadFile=File(...)):
    task_name = "classify.task"
    task = celery.send_task(task_name, args=[img.filename])
    #return task
    return dict(id=task.id, url='localhost:5000/check_task/{}'.format(task.id))

@app.post("/image/")
async def classify_image(img:UploadFile=File(...)):
    output = BytesIO()
    im=Image.open(img.file)
    im.save(output, format=im.format)

    redis_store.set(img.filename,output.getvalue())
    
    task_name = "classify.task"
    task = celery.send_task(task_name, args=[img.filename])
    result=task.get()
    ret={}
    ret[img.filename]=result
    return ret
    #return img.filename
@app.post("/multiple_images/")
async def classify_image(files:List[UploadFile]=File(...)):
    ret={}
    for file in files:
        output = BytesIO()
        im=Image.open(file.file)
        im.save(output, format=im.format)

        redis_store.set(file.filename,output.getvalue())
        sleep(2)
        task_name = "classify.task"
        task = celery.send_task(task_name, args=[file.filename])
        ret[file.filename]=task.get()
    return ret
@app.get("/check_task/{id}")
def check_task(id: str):
    task = celery.AsyncResult(id)
    if task.state == 'SUCCESS':
        response = {
            'status': task.state,
            'result': task.result,
            'task_id': id
        }
    elif task.state == 'FAILURE':
        response = json.loads(task.backend.get(task.backend.get_key_for_task(task.id)).decode('utf-8'))
        del response['children']
        del response['traceback']
    else:
        response = {
            'status': task.state,
            'result': task.info,
            'task_id': id
        }
    return response
