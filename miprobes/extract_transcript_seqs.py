#conda install -c bioconda pyensembl
#pyensembl install --release 75 --species human

import pyensembl as pe
import pandas as pd

ensembl = pe.EnsemblRelease(99)

outputfile = open('output.fasta', 'w')

meta = pd.read_csv('meta.csv', low_memory=False)
gene_ids = meta['ID'].tolist()

for gene in gene_ids:
    transcript_ids = ensembl.transcript_ids_of_gene_id(gene)
    for transcript_id in transcript_ids:
        seq = ensembl.transcript_sequence(transcript_id)
        outputfile.write(">" + gene + '_' + transcript_id + '\n')
        outputfile.write(seq + '\n')
