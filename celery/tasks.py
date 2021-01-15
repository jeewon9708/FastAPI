import tensorflow.keras as keras
import tensorflow as tf
from time import sleep
import traceback
import redis
from PIL import Image
from celery import current_task
from celery import states
from celery.exceptions import Ignore
from tensorflow.keras.models import model_from_json
from worker import celery

from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO


redis_store = redis.Redis.from_url("redis://redis_server:6379/10")
#from app.worker import Photo


@celery.task(name='hello.task', bind=True)
def hello_world(self, name):
    try:
        if name == 'error':
            k = 1 / 0
        for i in range(60):
            sleep(1)
            self.update_state(state='PROGRESS', meta={'done': i, 'total': 60})
        return {"result": "hello {}".format(str(name))}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

@celery.task(name='bye.task', bind=True)
def bye_world(self, name):
    try:
        if name == 'error':
            k = 1 / 0
        for i in range(60):
            sleep(1)
            self.update_state(state='PROGRESS', meta={'done': i, 'total': 60})
        return {"result": "hello {}".format(str(name))}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex

@celery.task(name='classify.task', bind=True)
def classify_img(self,filename):
  
    MY_GRAPH = tf.compat.v1.get_default_graph()
    
    json_file = open("model.json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("model.h5")
    image=Image.open(BytesIO(redis_store.get(filename)))
    image=image.resize((150,150))
    image=np.array(image)
    image=image[...,:3]
    image=np.expand_dims(image, axis=0)
    images = np.vstack([image])
    images=images/255

    with MY_GRAPH.as_default():
        json_file = open("model.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights("model.h5")
        model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['acc'])
        classes=model.predict(images)
    if classes[0]>0.5:
        return "human"
    else:
        return "horse"
    
    