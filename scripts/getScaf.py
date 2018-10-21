#!/usr/bin/env python
# encoding: utf-8
"""
getRead.py

Created by www on  5:02 pm, Sep 11, 2018
"""
import numpy as np 
import sys
import os
from Bio import SeqIO
 
 
def loadRef(reference):
    refs    = {}
    for r in SeqIO.parse(reference, 'fasta'):
        refs[str(r.id)] = r.seq
    return refs

def loadFile(refs, inputFile, outputDir):
    scaff =  {}
    with open(inputFile) as f:
        for line in f:
            line    = line.strip()
            if not line:
                continue
            info    = line.split()
            ref     = info[0]
            scaff[ref] = ''
    
    for ref in scaff:
        outputFile = os.path.join(outputDir, ref)
        o          = open(outputFile, 'w+')
        o.write('>%s\n%s\n' % (ref, refs[ref]))

        o.close()


def main():
    inputFile      = sys.argv[1]
    outputDir      = sys.argv[2]
    reference      = sys.argv[3]

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
    refs    = loadRef(reference)
    loadFile(refs, inputFile, outputDir) 
 
if __name__ == '__main__':
    main()

