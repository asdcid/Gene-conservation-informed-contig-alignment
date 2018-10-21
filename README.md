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
git clone https://github.com/asdcid/.git
```


## Usage
This method requires a genome assembly (fasta format) and a whole set of gene nt sequences (fasta format) from the same species or shorter evolutionary distance species. 
