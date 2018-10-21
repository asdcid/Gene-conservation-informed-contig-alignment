# Haplotig-separation
Separation haplotigs from the genome assembly

## Introduction
Some regions of genome are highly heterozygous, which contain two alleles at the same gene locus (we called it ‘primary contigs’ and associated ‘haplotigs’ according to FALCON_unzip (https://github.com/PacificBiosciences/FALCON_unzip/)). Assemblers may produce both primary contig and haplotig without labelling instead of a single haplotype-fused contig. Those ‘unidentified’ haplotigs may cause issues in the downstream analyses. Some tools are developed for separating the primary contigs and haplotigs from the assembly, such as Purge Haplotigs (https://bitbucket.org/mroachawri/purge_haplotigs), HaploMerger2 (https://github.com/mapleforest/HaploMerger2/releases/) or FALCON_unzip. Purge Haplotigs remapped short-reads or long-reads to obtain the coverage information for haplotigs separation, whereas HaploMerger2 separated haplotigs basing on all-against-all whole genome alignment. 

Here, we developed a new and quick method separated haplotigs basing on sequence similarity. The idea is simple: we use gene nt sequences (can be from the same species or shorter evolutionary distance species) as the marker, mapped the marker to the assembly. If a contig (haplotig) is associated to another contig (primary contig), most of regions of them should be very similarity even the same. Therefore, we can find the same marker between them. One drawback of this method may not work for those contigs that do not contain any genes.


## Requirments
- Python 2.7 or higher
- BLAST 2.2.30+
- Mummer 4.0


## Installation
No installation required, just download the pipeline from github.
```
https://github.com/asdcid/Haplotig-separation.git
```

## Usage
This method requires a genome assembly (fasta format) and a whole set of gene nt sequences (fasta format) from the same species or shorter evolutionary distance species. 

The path of BLAST and Mummer should be set into the environment path first, or change "export PATH=xxxx" in the run.sh. In addition, only the path of **genome**, **genes** and **outputDir** needed to be set. other parameters can use default.
```
#############################################
#set path of Mummer
export PATH='/path/of/mummer/':$PATH
#set path of Blast
export PATH='/path/of/blast/':$PATH

#the path of genome assembly file, fasta format
genome='../ori/canu_1kb.fa'

#the path of gene nt sequence, fasta format
genes='../Egra_gene/gene.fa'

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
minCoverge=80

#############################################
```

After modify the run.sh script, just directly run **./run.sh**.
