from time import sleep
from uuid import uuid4
from . import celery_in


@celery_in.task
def async_uuid_generation(delay:int):
    sleep(delay)
    return str(uuid4())


def get_unique_id_with_delay(delay:int):
    '''returns uuid4 after delay in seconds
    NOTE: invokes async_uuid_generation, which is a celery worker task'''
    async_uuid_generation(delay)