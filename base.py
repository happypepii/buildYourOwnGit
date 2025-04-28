import os
import data

FILES_TO_IGNORE = ['.mygit', '.git', '.gitignore', '__pycache__']

def write_tree(directory='.'):
    entries = []
    
    for entry in os.scandir(directory):
        if entry.name in FILES_TO_IGNORE:
            continue
        
        entry_path = os.path.join(directory, entry.name)
        
        if entry.is_file():
            with open(entry_path, 'rb') as f:
                blob_oid = data.hash_object(f.read(), type_='blob')
            entries.append(f'blob {blob_oid} {entry.name}')
        
        elif entry.is_dir():
            tree_oid = write_tree(entry_path)
            entries.append(f'tree {tree_oid} {entry.name}')
    
    tree_content = '\n'.join(entries).encode()
    tree_oid = data.hash_object(tree_content, type_='tree')
    
    return tree_oid

def read_tree(objectId, directory='.'):
    tree_data = data.cat_file(objectId, 'tree').decode()
    entries = tree_data.split('\n')
    
    for entry in entries:
        type_, objectId, name = entry.split()
        
        if type_ == 'tree':
            new_path = os.path.join(directory, name)
            os.makedirs(new_path, exist_ok=True)
            read_tree(objectId, new_path)
        
        elif type_ == 'blob':
            path = os.path.join(directory, name)
            with open(path, 'wb') as f:
                f.write(data.cat_file(objectId))
                