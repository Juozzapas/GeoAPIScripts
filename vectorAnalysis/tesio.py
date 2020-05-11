#! /usr/bin/env python3

import sys
import os
cwd = os.getcwd()

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
print(cwd)
print(sys.path)