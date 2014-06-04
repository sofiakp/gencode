import sys
import argparse 
import fileinput
from argparse import RawTextHelpFormatter

desc = """Splits genes into three bins:
- A bin [-w, +w] around the TSS
- A bin [-w, +w] around the TES
- The rest of the gene body

These are written into three different output files. The first two bins do 
not extend beyond the middle of the gene. If the gene is too short, then the
last window (rest of gene body) might be empty, so nothing will be written
for that gene.

The input should be BED-like. Reads from STDIN.
"""
parser = argparse.ArgumentParser(description = desc, formatter_class = RawTextHelpFormatter)
parser.add_argument('tss_file')
parser.add_argument('tes_file')
parser.add_argument('rest_file')
parser.add_argument('-w', '--win', type = int)
args = parser.parse_args()
w = args.win

with open(args.tss_file, 'w') as tss_file, \
        open(args.tes_file, 'w') as tes_file, \
        open(args.rest_file, 'w') as rest_file:
    for line in fileinput.input([]):
        fields = line.strip().split()
        start = int(fields[1])
        end = int(fields[2])
        strand = fields[5]
        middle = int((start + end) /  2) 

        if strand == '+':
            tss_start = max(0, start - w)
            tss_end = min(middle, start + w)
            
            tes_start = max(middle, end - w)
            tes_end = end + w

            rest_start = tss_end 
            rest_end = tes_start
        else:
            tss_start = max(middle, end - w)
            tss_end = end + w

            tes_start = max(0, start - w)
            tes_end = min(middle, start + w)

            rest_start = tes_end
            rest_end = tss_start

        fields[1] = str(tss_start)
        fields[2] = str(tss_end)
        tss_file.write('\t'.join(fields) + '\n')

        fields[1] = str(tes_start)
        fields[2] = str(tes_end)
        tes_file.write('\t'.join(fields) + '\n')

        if rest_start < rest_end:
            fields[1] = str(rest_start)
            fields[2] = str(rest_end)
            rest_file.write('\t'.join(fields) + '\n')   
