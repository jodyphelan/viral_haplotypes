# viral_haplotypes


#### Prerequisites
* samtools
* python

#### Parameters

```
extract_haplotypes.py <bam> <ref_name> <start> <end> <out_prefix> [--bam]

bam		bam file
ref_name 	name of the sequence 
start		start coordinate
end		end coordinate
out_prefix	prefix for outfiles
--bam		[optional] output reduced bam file
```

The ```--bam``` flag is optional of you want to output the reduced bam for viualisation
