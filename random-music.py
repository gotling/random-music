#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import random
import shutil

# Settings
src='/Users/gotling/Sandbox/random-music/input'
dst='/Users/gotling/Sandbox/random-music/output'
max_size=512

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

def random_walk(directory):
    if(is_top_dir(directory)):
        copy_folder(directory)
    else:
        random_walk(os.path.join(directory, random.choice(get_folders(directory))))

def copy_folder(directory):
    if not os.path.exists(os.path.join(dst, os.path.basename(directory))):
        print os.path.basename(directory)
        shutil.copytree(directory, os.path.join(dst, os.path.basename(directory)))

def space_left(directory):
    return get_size(directory) < max_size * 1024 * 1024

def main():
    print "Random Music by Marcus Götling, www.gotling.se\n"
    
    print "Input:    ", src
    print "Output:   ", dst
    print "Max Size: ", max_size, "MiB\n"

    remove_and_create_folder(dst)

    while space_left(dst):
        random_walk(src)
    
    print "\nDone. Destination size: %s MiB" % (get_size(dst) / 1024 / 1024)
    
if __name__ == '__main__':
    main()