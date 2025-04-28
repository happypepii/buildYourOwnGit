import argparse
import os
import data
import base

def main():
    args = parse_args()
    args.func(args)

def parse_args():
    parser = argparse.ArgumentParser(description="This is a git-like tool")
    
    commands = parser.add_subparsers(dest='command')
    commands.required = True

    init_parser = commands.add_parser('init')
    init_parser.set_defaults(func=init)

    hash_parser = commands.add_parser('hash-object')
    hash_parser.set_defaults(func=hash_object)
    hash_parser.add_argument('file', help='File to hash')

    cat_file_parser = commands.add_parser('cat-file')
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument('objectId')

    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = commands.add_parser('read-tree')
    read_tree_parser.add_argument('objectId')
    read_tree_parser.set_defaults(func=read_tree)

    return parser.parse_args()

def init(args):
    data.init()

def hash_object(args):
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))

def cat_file(args):
    content = data.cat_file(args.objectId, expected=None)
    if content is None:
        print(f"Object {args.objectId} not found")
    else:
        print(content.decode())

def write_tree(args):
    print(base.write_tree())

def read_tree(args):
    base.read_tree(args.objectId)
        
if __name__ == "__main__":
    main()