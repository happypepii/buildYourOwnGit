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
