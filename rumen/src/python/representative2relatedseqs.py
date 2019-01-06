
import pandas as pd

df = pd.read_csv('dataflow/03-blast-tables/lacto_signal_differential_mapped', sep='\t', low_memory=False, names=["qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq"])

df = df[(df['length'] == 190)]
df = df[(df['pident'] >= 99)]

with open('dataflow/01-nucl/lacto_signal_differential_all_seqs.fasta', 'w') as file:
    for index, row in df.iterrows():
    
        header = row['sseqid']
        asv_id_short = header.split('_')[0][0:5]
        tag = header.split('_')[1]
    
        header_short = ">" + asv_id_short + "_" + tag
        file.write(header_short + "\n")
    
        seq = row['sseq'].replace("-", "")
        file.write(seq + "\n")

    