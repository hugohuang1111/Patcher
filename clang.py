#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
sys.path.append("..")
from clang import cindex

def showToken(node):
    ts=node.get_tokens()
    for t in ts:
        print t.spelling

def main():
    print 'entry clang'
    cur_dir = os.path.split(os.path.realpath(__file__))[0]
    if platform.system() == 'Darwin':
        libclang_dylib_dir = os.path.join(cur_dir, 'libclang')
        cindex.Config.set_library_path(libclang_dylib_dir)

    index = cindex.Index.create()
    tu = index.parse("main.cpp")
    showToken(tu.cursor)
    print 'exit clang'

if __name__ == '__main__':
    main()

