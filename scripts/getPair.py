#!/usr/bin/env python
# encoding: utf-8
"""
getRef.py

Created by www on 11:32 pm, Sep 11, 2018
"""
import numpy as np 
import sys
import os

 
def loadFile(inputFile, outputFile):
    o   = open(outputFile, 'w+')
    with open(inputFile) as f:
        for line in f:
            line    = line.strip()
            if not line:
                o.write('\n')
                continue
            info    = line.split()
            o.write('%s\t' % info[0])

    o.close()
 
def main():
    inputFile    = sys.argv[1]
    outputFile   = sys.argv[2]
    
    loadFile(inputFile, outputFile) 
 
if __name__ == '__main__':
    main()

