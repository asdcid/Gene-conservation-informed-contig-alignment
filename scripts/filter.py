#!/usr/bin/env python
# encoding: utf-8
"""
phase.py

Created by www on  1:48 pm, Sep 11, 2018
"""
import numpy as np 
import sys
import os
from Bio import SeqIO
 
def loadFile(inputFile, genes, minAlignLength):
    refs        = {}
    with open(inputFile) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue    
            info    = line.split()
            geneID  = info[0]
            ref     = info[1]
            identity    = float(info[2])

            alignLenth  = int(info[3])
            coverage    = alignLenth * 1.0 / genes[geneID]
            if coverage < minAlignLength:
                continue
            if not ref in refs:
                refs[ref] = {}
            #only get the first (which is also the best) location
            if not geneID in refs[ref]:
                refs[ref][geneID] = ''
    return refs


def phase(refs, outputFile, genome, minGene, minGeneCover):
    o   = open(outputFile, 'w+')
    refNames    = []
    for ref in refs:
        if ref in refNames:
            continue
        refNames.append(ref)
        if len(refs[ref]) < minGene:
            continue
        for compareRef in refs:
            matchGenes = []
            if compareRef in refNames:
                continue
            if len(refs[compareRef]) < minGene:
                continue
            for geneID in refs[compareRef]:
                if geneID in refs[ref]:
                    matchGenes.append(geneID)
            number  = len(matchGenes)
            if number >= minGene:
                if number / len(refs[ref]) * 1.0 >= minGeneCover or number / len(refs[compareRef]) *1.0 >= minGeneCover:
                    o.write('%s\t%d\t%d\t%d\t' % (ref, len(refs[ref]), number, genome[ref]))
                    #for gene in matchGenes:
                    #    o.write('%s\t' % gene)
                    o.write('\n')
                    o.write('%s\t%d\t%d\t%d\n' % (compareRef, len(refs[compareRef]), number, genome[compareRef]))
                    o.write('\n')

    o.close()

def loadGene(geneFile):
    genes   = {}
    for r in SeqIO.parse(geneFile, 'fasta'):
        genes[str(r.id)] = len(r.seq)
    return genes
 
def main():
    inputFile   = sys.argv[1]
    outputFile  = sys.argv[2]
    genomeFile  = sys.argv[3]
    geneFile    = sys.argv[4]
    minGene         = float(sys.argv[5])
    minAlignLength  = float(sys.argv[6])
    minGeneCover    = float(sys.argv[7])

    
   
  
 
    genome  = loadGene(genomeFile)
    genes   = loadGene(geneFile)
    refs    = loadFile(inputFile, genes, minAlignLength) 
    phase(refs, outputFile, genome, minGene, minGeneCover)



 
if __name__ == '__main__':
    main()

