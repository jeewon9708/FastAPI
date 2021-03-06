import os
from celery import Celery

#CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redis_server:6379")
#CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redis_server:6379")

#celery = Celery("celery", backend=CELERY_BROKER_URL, broker=CELERY_RESULT_BACKEND)


celery = Celery("celery", backend='amqp://guest:guest@rabbitmq_server:5672', broker='amqp://guest:guest@rabbitmq_server:5672')
