import os
import hashlib

GIT_DIR = '.mygit'

def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')
    print("Initialized empty mygit repository in .mygit")

def hash_object(content, type_='blob'):
    obj = type_.encode() + b'\0' + content    
    objectId = hashlib.sha1(obj).hexdigest()
    with open(f'{GIT_DIR}/objects/{objectId}', 'wb') as f:
        f.write(obj)
    return objectId

def cat_file(objectId, expected='blob'):
    try:
        with open(f'{GIT_DIR}/objects/{objectId}', 'rb') as f:
            obj = f.read()
        type_, _, content = obj.partition(b'\0')
        type_ = type_.decode()
        
        if expected is not None and expected != type_:
            raise ValueError(f"Expected {expected}, but got {type_}")
        
        return content

    except FileNotFoundError:
        return None