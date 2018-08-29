import os
from .settings import *

# Debug methods

def known_robots():
    root, robots, files = next(os.walk(ROBOTS_DIRECTORY))
    return robots

def print_known_robots():
    print("\nknown robots:\n")
    for robot in known_robots(): print("\t * "+robot)
    print("\n")
