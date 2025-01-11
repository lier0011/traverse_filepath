#!/usr/bin/env python3

import sys
import os
import optparse

def traverse(path, limit_count, limit_min_file_size, file_type):
    print("traversing the path: " + path)
    print("limit_count: " + str(limit_count))
    print("limit_min_file_size: " + str(limit_min_file_size))
    if file_type is not None:
        print("file_type: " + str(file_type))

    _list = []
    counter = 0
    for _root, _dir, _files in os.walk(path):
        for file in _files:
            abs_path = os.path.join(_root, file)
            stat = os.stat(abs_path)
            # we only get file with this limit min size
            if stat.st_size > limit_min_file_size:
               # flag to insert
               insert_rec = 1
               # if this filter is activated and there is no match, then don't save it
               if file_type is not None and not file.lower().endswith("." + file_type.lower()):
                  insert_rec = 0

               if insert_rec == 1:
                  _list.append((file, abs_path, stat.st_size))

            # if we reach the limit_count, than stop it
            if len(_list) == limit_count:
                break
        if len(_list) == limit_count:
            break

    return _list

if __name__ == "__main__":
    LIMIT_COUNT = 5
    LIMIT_MIN_FILE_SIZE = 100000

    parser = optparse.OptionParser()
    parser.add_option('-p', '--path', help='specify the path to traverse, default: current directory')
    parser.add_option('-c', '--limit_count', help='limited number of results, default: {}'.format(LIMIT_COUNT))
    parser.add_option('-f', '--limit_min_file_size', help='minimum limit of the file size in bytes, default: {}'.format(LIMIT_MIN_FILE_SIZE))
    parser.add_option('-t', '--file_type', help='filter based on a specific file type, default: all files')
    opts, args = parser.parse_args()
    if opts.path is None:
        opts.path = "."
    if opts.limit_count is None:
        opts.limit_count = LIMIT_COUNT
    if opts.limit_min_file_size is None:
        opts.limit_min_file_size = LIMIT_MIN_FILE_SIZE

    files = traverse(opts.path, int(opts.limit_count), int(opts.limit_min_file_size), opts.file_type)
    if len(files) == 0:
        print("no files found matching the criteria")
    else:
        print("this is what we found:")
        for file in files:
            print(file)
