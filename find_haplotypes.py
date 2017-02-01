import sys
import subprocess
import re
from collections import defaultdict

if len(sys.argv)<5:
	print """
extract_haplotypes.py <bam> <ref_name> <start> <end> <out_prefix> [--bam]

bam		bam file
ref_name 	name of the sequence 
start		start coordinate
end		end coordinate
out_prefix	prefix for outfiles
--bam		[optional] output reduced bam file
"""
	quit()


script,bam,sname,start,end,out = sys.argv[:6]
start = int(start)
end = int(end)


def index_bam(infile):
	import os
	idx = infile+"bai"
	if not os.path.isfile(idx):
		subprocess.call("samtools index %s " % (infile),shell=True)

haplotypes = defaultdict(int)
index_bam(bam)
cmd = subprocess.Popen("samtools view -h %s %s:%s-%s" % (bam,sname,start,end),shell=True,stdout=subprocess.PIPE)
bam_lines = []
for l in cmd.stdout:
	if l[0]=="@":
		bam_lines.append(l.rstrip())
		continue
	arr = l.split()
	start_pos = int(arr[3])
	end_pos = start_pos
	for x in re.findall("(\d+\w)",arr[5]):
		re_obj = re.match("(\d+)(\w)",x)
		for i in range(int(re_obj.group(1))):
			if re_obj.group(2)=="M":
				end_pos+=1
			elif re_obj.group(2)=="D":
				end_pos+=1
			
	if start_pos<start and end_pos>end:
		bam_lines.append(l.rstrip())
		seq = []
		for i in range(start-start_pos,len(arr[9])-(end_pos-end)):
			seq.append(arr[9][i])
		haplotypes["".join(seq)]+=1

with open(out+".fa","w") as o:
	for i,h in enumerate(haplotypes):
		o.write(">haplo_%s_freq_%s\n%s\n" % (i,haplotypes[h],h))

if "--bam" in sys.argv:
	samname = out+".sam"
	bamname = out+".bam"
	with open(samname,"w") as o:
		for l in bam_lines:
			o.write(l+"\n")
	subprocess.call("samtools view -Sb %s > %s" % (samname,bamname),shell=True)
	subprocess.call("rm %s" % samname,shell=True)
