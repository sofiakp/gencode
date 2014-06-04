import sys
import fileinput

for line in fileinput.input():
    fields = line.strip().split('\t')
    if fields[2] == 'transcript':
        sub = fields[8].split()
        gene = ''
        for idx, s in enumerate(sub):
            if s.strip() == 'gene_name':
                gene = sub[idx + 1].strip('";').strip('"')
                break
        if gene != '':
            print '\t'.join([fields[0], fields[3], fields[4], fields[6], gene])
