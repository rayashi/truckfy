import os
from uuid import uuid4


def truck_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}-{}.{}'.format(instance.id, uuid4().hex, ext)
    return os.path.join("trucks", filename)


def client_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}-{}.{}'.format(instance.id, uuid4().hex, ext)
    return os.path.join("clients", filename)


def get_first_name(full_name):
    if len(full_name.split(' ', 1)) >= 2:
        first_name = full_name.split(' ', 1)[0]
    else:
        first_name = full_name.split(' ', 1)[0]
    return first_name


def get_last_name(full_name):
    if len(full_name.split(' ', 1)) >= 2:
        last_name = full_name.split(' ', 1)[1]
    else:
        last_name = ''
    return last_name
