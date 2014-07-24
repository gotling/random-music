#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Random Music by Marcus Götling, www.gotling.se

Usage:
    random-music.py <src> <dst> <size> [--delete]

Options:
    --delete  Remove and recreate destination folder before copying files.
"""

import os
import random
import shutil
from docopt import docopt

def regular_file(item):
    return not item.startswith('.')

def get_folders(directory):
    f = []
    d = []
    for (dirpath, dirname, filename) in os.walk(directory):
        f.extend(filename)
        d.extend(dirname)
        break
    return d

def remove_and_create_folder(directory):
    shutil.rmtree(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def is_top_dir(directory):
    return len(get_folders(directory)) == 0

def random_walk(source, destination):
    if(is_top_dir(source)):
        copy_folder(source, destination)
    else:
        random_walk(os.path.join(source, random.choice(get_folders(source))), destination)

def copy_folder(source, destination):
    if not os.path.exists(os.path.join(destination, os.path.basename(source))):
        print os.path.basename(source)
        try:
        	shutil.copytree(source, os.path.join(destination, os.path.basename(source)))
        except Exception as e:
        	print "Could not copy folder '%s'" % source

def space_left(directory, max_size):
    return get_size(directory) < max_size * 1024 * 1024

def main():
    arguments = docopt(__doc__, version='Random Music 0.1')

    if (arguments["--delete"]):
        remove_and_create_folder(arguments["<dst>"])

    while space_left(arguments["<dst>"], arguments["<size>"]):
        random_walk(arguments["<src>"], arguments["<dst>"])
    
    print "\nDone. Destination size: %s MiB" % (get_size(arguments["<dst>"]) / 1024 / 1024)
    
if __name__ == '__main__':
    main()
