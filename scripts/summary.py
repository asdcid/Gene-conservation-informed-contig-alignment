#!/usr/bin/env python
# encoding: utf-8
"""
parse.py

Created by www on 12:24 pm, Sep 13, 2018
"""
from __future__ import print_function
import numpy as np 
import sys
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

 
def loadFile(inputFile, s, coverages, identity, coverage, coverageFilter):
    coverageMark    = False
    coverageStart   = False
    with open(inputFile) as f:
        for line in f:
            line    = line.strip()
            if not line:
                continue
            info    = line.split()
            if info[0] == '[Bases]':
                coverageStart    = True
            #if info[0] == 'TotalBases' and coverageStart:
            #    refLen  = int(info[1])
            #    qryLen  = int(info[2])
            #    if refLen > qryLen:
            #        longer  = 'ref'
            #    else qryLen > refLen:
            #        longer  = 'qry'
            
            if info[0] == 'AlignedBases' and coverageStart:
                coverageStart = False
                refCoverage     = float(info[1].split('(')[1].split('%')[0])
                qryCoverage     = float(info[2].split('(')[1].split('%')[0])
                if refCoverage == 0 and qryCoverage == 0:
                    return coverages, identity, coverageFilter
                coverages['ref'].append(refCoverage)
                coverages['qry'].append(qryCoverage)
                if refCoverage >= coverage or qryCoverage >= coverage:
                    coverageMark    = True             
            if info[0] == '1-to-1':
                identityKey     = '1'
            if info[0] == 'M-to-M':
                identityKey     = 'm'
            if info[0] == 'AvgIdentity':
                refIdentity     = float(info[1])
                qryIdentity     = float(info[2])
                if refIdentity != qryIdentity:
                    print('Key different')
                    print(inputFile)
                    sys.exit() 
                identity[identityKey].append(refIdentity)            
               
                if coverageMark:
                    coverageFilter[identityKey].append(refIdentity)
 
                if identityKey == 'm':
                    if coverageMark:
                        refName, qryName     = inputFile.split('/')[-1].split('.')[0].split('_')
                        s.write('%s\t%s\t%.2f\t%.2f\t%.2f\t%.2f\n' % (refName, qryName, refCoverage, qryCoverage, identity['1'][-1], identity['m'][-1]))
                    return coverages, identity, coverageFilter
def plot(data, key, name, outputDir):
    plt.figure(key+name+outputDir)
    plt.title('Distribution of %s (%s)' % (name, key))
    plt.hist(data, bins=50)
    outputFile  = os.path.join(outputDir, '%s_%s.png' % (name, key))
    plt.savefig(outputFile)

def main():
    inputDir       = sys.argv[1]
    outputDir      = sys.argv[2] 
    coverage       = float(sys.argv[3])


    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)


    s   = open(os.path.join(outputDir,  'summary'), 'w+')
    s.write('refName\tqryName\trefCoverage\tqryCoverage\tidentity(1-to-1)\tidentity(m-to-m)\n')

    coverages   = {
                   'ref' : [], 
                   'qry' : []
                  }

    identity    = {
                    '1' : [],
                    'm' : []
                  }

    coverageFilter = {
                        '1' : [],
                        'm' : []
                     }

    f   = os.walk(inputDir)
    for root, dirs, names in f:
        for name in names:
            if name.split('.')[-1] == 'report': 
                inputFile   = os.path.join(root, name)
                #print(inputFile)
                coverages, identity, coverageFilter = loadFile(inputFile, s, coverages, identity, coverage, coverageFilter)
                
    for key in coverages:
        plot(coverages[key], key, 'Coverage', outputDir)
    
    for key in identity:
        plot(identity[key], key, 'Identity', outputDir)

    for key in coverageFilter:
        plot(coverageFilter[key], key, 'Identity after coverage filtered', outputDir)
    s.close() 

if __name__ == '__main__':
    main()

