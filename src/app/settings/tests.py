from .development import *  # noqa

for queueConfig in RQ_QUEUES.values():
    queueConfig['ASYNC'] = False
