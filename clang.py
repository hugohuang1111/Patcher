#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from clang import cindex

def showToken(node):
    ts=node.get_tokens()
    for t in ts:
        print t.spelling

def main():
    print 'entry clang'
    index = cindex.Index.create()
    tu = index.parse("ToyClangPlugin.cpp")
    showToken(tu.cursor)
    print 'exit clang'

if __name__ == '__main__':
    main()

