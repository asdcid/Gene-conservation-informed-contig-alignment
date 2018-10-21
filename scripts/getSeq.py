#!/usr/bin/env python
# encoding: utf-8
"""
get primary.fasta and haplotigs.fasta

Created by www on  3:29 pm, Sep 13, 2018
"""
import numpy as np 
import sys
import os
from Bio import SeqIO

minIdentity     = 95 

def loadRef(genome):
    refs    = {}
    for r in SeqIO.parse(genome, 'fasta'):
        refs[str(r.id)] = r.seq
    return refs
 
    
def loadFile(refs, separateFile, outputFile, primary, haplotigs):
    pris    = {}
    haps    = {}
    with open(separateFile) as f:
        for line in f:
            line    = line.strip()
            if not line:
                continue
            info    = line.split()
            ref     = info[0]
            if ref == 'refName':
                continue
            qry     = info[1]
            refCov  = float(info[2])
            qryCov  = float(info[3])
            refLen  = len(refs[ref])
            qryLen  = len(refs[qry])
            refId   = float(info[4])
            qryId   = float(info[5])

            if refId < minIdentity or qryId < minIdentity:
                continue            
 
            if qryCov < refCov:
                ref, qry        = qry, ref
                refCov, qryCov  = qryCov, refCov
            if not ref in pris:
                pris[ref] = {}
            pris[ref][qry] = ''
                    
            haps[qry] = ''
    
    #debug
    for ref in pris:
        if ref in qry:
            print('Reference %s in both primary and haptigs' % ref)
            

    o = open(outputFile, 'w+')
    o.write('Primary(length)\thaptigs(length)\n')
    for ref in pris:
        o.write('%s (%d)\t<===\t' % (ref, len(refs[ref])))
        for hap in pris[ref]:
            o.write('%s (%d)\t' % (hap, len(refs[hap])))
        o.write('\n')
    o.close()
    
    p   = open(primary, 'w+')
    h   = open(haplotigs, 'w+')
    for ref in refs:
        if ref in haps:
            h.write('>%s\n%s\n' % (ref, refs[ref]))
        else:
            p.write('>%s\n%s\n' % (ref, refs[ref]))

    p.close()
    h.close()


def main():
    inputDir       = sys.argv[1]
    outputDir      = sys.argv[1]
    genome         = sys.argv[2]

   
    primary         = os.path.join(outputDir, 'primary.fasta')
    haplotigs       = os.path.join(outputDir, 'haplotigs.fasta')
    outputFile      = os.path.join(outputDir, 'separate_info') 
    separateFile    = os.path.join(inputDir, 'summary')

    refs    = loadRef(genome)
    loadFile(refs, separateFile, outputFile, primary, haplotigs)


if __name__ == '__main__':
    main()

