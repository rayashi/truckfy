import os
from uuid import uuid4


def truck_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    path = os.path.join("trucks", str(instance.id))
    return os.path.join(path, filename)


def client_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}-{}.{}'.format(instance.id, uuid4().hex, ext)
    return os.path.join("clients", filename)
