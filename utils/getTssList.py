import sys

with open(sys.argv[1], 'r') as infile:
    for line in infile:
        fields = line.strip().split()
        if line[0] == '#' or fields[2] != 'transcript':
            continue
        tid = ''
        gid = '-'
        gene = '-'
        for idx, annot in enumerate(fields[8:-1]):
            if annot == 'transcript_id':
                tid = fields[idx + 9].strip(';').strip('"')
            elif annot == 'gene_id':
                gid = fields[idx + 9].strip(';').strip('"')
            elif annot == 'gene_name':
                gene = fields[idx + 9].strip(';').strip('"')
        if tid != '':
            print '\t'.join([fields[0], str(int(fields[3]) - 1), fields[4], tid, '.', fields[6], gid, gene])
