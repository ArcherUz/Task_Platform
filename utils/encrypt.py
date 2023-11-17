import hashlib
import uuid
from django.conf import settings
def md5(string):
    hash_obj = hashlib.md5(settings.SECRET_KEY.encode('UTF-8'))
    hash_obj.update(string.encode('UTF-8'))
    return hash_obj.hexdigest()

def uid(string):
    data = "{}-{}".format(uuid.uuid4(), string)
    return md5(data)