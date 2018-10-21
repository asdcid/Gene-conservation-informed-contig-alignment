#!/bin/bash



inputDir=$1
figureDir=$2
outputDir=$3

inputFile=$inputDir/summary
mkdir -p $outputDir    

while read -r ref qry refCov qryCov refId1 refIdm 
do
    if [ $ref == 'refName' ]
    then
        continue
    fi
    name=${ref}_${qry}.png
    cp $figureDir/$name $outputDir/

done <$inputFile
