# Gene conservation informed contig alignment (GCICA)
Separation haplotigs from the genome assembly

## Introduction
Some regions of genome are highly heterozygous, which contain two alleles at the same gene locus (we called it ‘primary contigs’ and associated ‘haplotigs’ according to FALCON_unzip (https://github.com/PacificBiosciences/FALCON_unzip/)). Assemblers may produce both primary contig and haplotig without labelling instead of a single haplotype-fused contig. Those ‘unidentified’ haplotigs may cause issues in the downstream analyses. Some tools are developed for separating the primary contigs and haplotigs from the assembly, such as Purge Haplotigs (https://bitbucket.org/mroachawri/purge_haplotigs), HaploMerger2 (https://github.com/mapleforest/HaploMerger2/releases/) or FALCON_unzip. Purge Haplotigs remapped short-reads or long-reads to obtain the coverage information for haplotigs separation, whereas HaploMerger2 separated haplotigs basing on all-against-all whole genome alignment. 

Here, we developed a new and quick method separated haplotigs basing on sequence similarity. The idea is simple: we use gene nt sequences (can be from the same species or shorter evolutionary distance species) as the marker, mapped the marker to the assembly. If a contig (haplotig) is associated to another contig (primary contig), most of regions of them should be very similarity even the same. Therefore, we can find the same marker between them. One drawback of this method may not work for those contigs that do not contain any genes.


## Requirments
- Python 2.7 or higher
- Matplotlib package (Python)
- BLAST 2.2.30+
- Mummer 4.0


## Installation
No installation required, just download the pipeline from github.
```
git clone https://github.com/asdcid/Gene-conservation-informed-contig-alignment.git
```

## Usage
This method requires a genome assembly (fasta format) and a whole set of gene nt sequences (fasta format) from the same species or shorter evolutionary distance species. 

The path of BLAST and Mummer should be set into the environment path first. 
```
Usage: GCICA -g assembly.fa -g genes.fa [options]

Required:
    -a      assembly file, fasta format
    -g      gene nt sequence file, fasta format

Options:
    -o      outputDir. Default is basename of assembly file + timestamp in the current directory
    -t      number of threads. Default is 10
    -i      minimun identity for blastn. Default is 80
    -m      the minimum number of aligned gene that each contig contains. Default is 3
    -l      the minimum fraction of aligned length in a gene. If the aligned length of a gene is lower than this fraction, this gene would not consider as a aligned gene. Deafult is 0.7
    -c      the percentage of minimum coverage between the possible primary and its associated haplotigs. Default is 80
    -f      fraction = the number of aligend gene in contig A which also aligned to contig B / total aligned gene in contig A. If the fracion > minGeneCover, these two contigs could be the possible primary contig and associated haplotig. Default is 0.8
```


## OutputFiles
The final result is in the final_result directory. 

**separate_info** file indicates the primary contigs and their associated haplotigs. 

**figures** directory is the dot-plot between primary contig and its associated haplotig. 

**summary** file is the datails of comparison between primary contigs and their associated haplotigs. 1-to-1: the unique mapping; m-to-m: the multiple mapping. Both 1-to-1, m-to-m and coverage information are from Mummer dnadiff result.
