#!/bin/bash

#$ -q hugemem.q
#$ -l virtual_free=10g,h_vmem=10.1g
#$ -pe threads 20
#$ -cwd
#$ -N default

set -e

#############################################
#set path of Mummer
export PATH='/home/rob/devel/mummer4/install/bin/':$PATH
export PATH='/home/raymond/devel/gnuplot/install/bin/':$PATH
#set path of Blast
export PATH='/path/of/blast/':$PATH

#the path of genome assembly file, fasta format
genome='../ori/canu_1kb.fa'

#the path of gene nt sequence, fasta format
genes='../Egra_gene/test.fa'

#the path of directory for storing output files, should be an empty directory
outputDir='result'

#how many CPU wants to use
threads=20

#minimum identity for blastn
minIdentity=0.8

#the minimum number of aligned gene that each contig contains
minGene=3

#the minimum fraction of aligned length in a gene. If the aligned length of a gene is lower than this fraction, this gene would not consider as a aligned gene.
minAlignLength=0.7

#fraction = the number of aligend gene in contig A which also aligned to contig B / total aligned gene in contig A. If the fracion > minGeneCover, these two contigs could be the possible primary contig and associated haplotig. 
minGeneCover=0.8

#the percentage of minimum coverage between the possible primary and its associated haplotigs
minCoverage=80

#############################################



mkdir -p $outputDir

#build index
reference=$(basename $genome)

cp $genome $outputDir/

makeblastdb \
    -in $outputDir/$reference \
    -dbtype nucl

echo "Finished step 1"

#blast
blastOutput=$outputDir/${reference%%.fa*}.blast.out

blastn \
    -query $genes \
    -db $outputDir/$reference \
    -out $blastOutput \
    -perc_identity $minIdentity \
    -evalue 1e-5 \
    -outfmt 7 \
    -num_threads $threads

#remove blast index
rm $outputDir/${reference}.nhr
rm $outputDir/${reference}.nin
rm $outputDir/${reference}.nsq

echo "Finished step 2"

#filter blast output
filterOutput=$outputDir/${reference%%.fa*}.filter.out
python filter.py \
    $blastOutput \
    $filterOutput \
    $outputDir/$reference \
    $genes \
    $minGene \
    $minAlignLength \
    $minGeneCover

echo "Finished step 3"
#get possible primary contig and its associated haplotig
pairOutput=$outputDir/${reference%%.fa*}.scaf.out
python getPair.py \
    $filterOutput \
    $pairOutput


echo "Finished step 4"

#make each contig in *.scaf.out into a single fasta file
scafOutputDir=$outputDir/scafs
python getScaf.py \
    $filterOutput \
    $scafOutputDir \
    $outputDir/$reference

echo "Finished step 5"

#plot the figure between possible primary contig and its associated haplotig, and get the coverage between them. Result in $outputDir/mummer_result and $outputDir/$mummer_plot
mummerOutput=$outputDir/mummer_result
mummerPlotOutput=$outputDir/mummer_plot
./mummer.sh \
    $pairOutput \
    $scafOutputDir \
    $mummerOutput \
    $mummerPlotOutput

echo "Finished step 6"

#summarize mummer result
summaryOutput=$outputDir/final_result
python summary.py \
    $mummerOutput \
    $summaryOutput \
    $minCoverage

echo "Finished step 7"

#move the dot-plot figure between primary contig and its associated haplotig to final_result directory.
figures=$summaryOutput/figures
./getFigure.sh \
    $summaryOutput \
    $mummerPlotOutput \
    $figures

echo "Finished step 8"

#get the primary.fasta and haplotigs.fasta
python getSeq.py \
    $summaryOutput \
    $outputDir/$reference 

echo "DONE"
