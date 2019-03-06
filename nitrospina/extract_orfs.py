import os, sys
from Bio.Seq import Seq
import pandas as pd

sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc

file = 'all_nitrospina_genomes.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location
outputfilename = file.split(".f")[0] + '_extractedORFs' + '.fasta'
file_obj.setOutputName(outputfilename)
file_obj.setOutputLocation('dataflow/01-prot/genes/')


def extractORFs_gff3(self, gff3_table_loc = 'dataflow/00-meta/all_nitrospina_genomes.csv'):

    fastadic = self.fasta2dict()
    outputfile = self.openwritefile()
    orfs_df = pd.read_csv(gff3_table_loc, low_memory=False)
    orfdic = dict()

    for index, row in orfs_df.iterrows():
        start = int(int(row['start']) - 1)
        end = int(row['end'])
        contig = row['contig']
        direction = row['direction']
        orf = row['ID']

        for k,v in fastadic.items():
            header = k.rstrip()
            if header == contig:
                seq = v.rstrip()
                seq_new = seq[start: end]
                if direction == '-':
                    seq_new_obj = Seq(seq_new)
                    seq_new_rc = str(seq_new_obj.reverse_complement())
                    orfdic.update({orf: seq_new_rc})
                else:
                    orfdic.update({orf: seq_new})

    for k,v in orfdic.items():
        header = k.rstrip()
        seq = v.rstrip()
        outputfile.write(">" + k + '\n')
        outputfile.write(v + '\n')

    #seq.complement()
    #seq.transcribe()
    #seq.translate()

file_obj.extractORFs_gff3()
