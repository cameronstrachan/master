import pandas as pd

#df = pd.read_csv('dataflow/03-blast-tables/lacto_signal_differential_all_seqs_tags_prevotella_genomes_mapped', sep='\t', low_memory=False, names=["qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq"])
#df['Database'] = 'Prevotella'
#df2 = pd.read_csv('dataflow/03-blast-tables/lacto_signal_differential_all_seqs_tags_rumen_genomes_mapped', sep='\t', low_memory=False, names=["qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq"])
#df2['Database'] = 'Rumen'

#df = df.append(df2)

df = pd.read_csv('dataflow/03-blast-tables/lacto_signal_differential_all_seqs_tags_rumen_genomes_mapped', sep='\t', low_memory=False, names=["qseqid", "sseqid", "pident", "sstart", "send", "qstart", "qend", "evalue", "bitscore", "score", "qlen", "length", "sseq"])
df['Database'] = 'Rumen'

df = df[(df['length'] >= 280)]
df = df[(df['pident'] >= 90)]

unique_seqs = list()

with open('dataflow/01-nucl/lacto_signal_differential_all_seqs_genomes.fasta', 'w') as file:
    for index, row in df.iterrows():
        
        unique_seq = row['sseqid']
      
        if (unique_seq in unique_seqs) != True:
            
            header = ">" + row['Database'] + "_" + row['sseqid']
            file.write(header + "\n")
    
            seq = row['sseq'].replace("-", "")
            file.write(seq + "\n")
        
            unique_seqs.append(unique_seq)
        

df_selected = df['sseqid'].str.rsplit('_', 1, expand = True)
df_selected.rename(columns={0:'Genome'}, inplace=True)
df_selected = df_selected['Genome']
df_selected = pd.DataFrame(df_selected.unique())
df_selected.rename(columns={0:'Genome'}, inplace=True)

df_selected.to_csv('dataflow/00-meta/selected_genomes.csv', header = True)


