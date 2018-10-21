#!/bin/bash

info=$1
scafs=$2
result=$3
plotDir=$4

name=$(basename ${info%%.scaf})
mkdir -p $result
mkdir -p $plotDir

while read -r qry ref
do
    name=$(basename ${qry})
    refName=$(basename $ref)
    #the prefix for output
    outputFile=$result/${refName}_$name
    outputPlotFile=$plotDir/${refName}_$name

    #echo $qry
    #echo $ref
    nucmer \
        --mum \
        --prefix=$outputFile  \
        $scafs/$ref \
        $scafs/$qry \

    mummerplot \
        --png \
        --prefix=$outputPlotFile \
        $outputFile.delta
    rm $plotDir/*gp
    rm $plotDir/*plot

    dnadiff -d $outputFile.delta \
        --prefix=$outputFile
    rm $outputFile.*diff
    rm $outputFile.1delta
    rm $outputFile.mdelta
    rm $outputFile.*coords
    rm $outputFile.snps

done <$info
