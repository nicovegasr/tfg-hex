import os
import sys

def add():
    parent_dir = os.path.dirname(os.path.realpath(__file__)).split('src')[0]
    for subdir, _, _ in os.walk(parent_dir):
        sys.path.append(subdir)
    