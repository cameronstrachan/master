# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

genomes_df = pd.read_csv('dataflow/00-meta/stewart2019_epsilonproteobacteria.csv', low_memory=False)
genomes = genomes_df['file_unzip'].tolist()

transcriptome_file = "11L2_ACAGTG.1.fastq.gz"
transcriptome = "dataflow/01-fastq/" + transcriptome_file

for genome in genomes:
    file = genome

    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    outputfilename = file.split(".f")[0] + '.gff3'
    file_obj.setOutputName(outputfilename)
    file_obj.setOutputLocation('dataflow/01-gff3/')
    file_obj.runprodigal(gff3 = True)

    outputfilename_sam = "dataflow/03-sam/" + transcriptome_file.split(".f")[0] + '_' + file.split(".f")[0] + ".sam"

    command = "bbmap.sh threads=60 ambig=random" + " " + "in=" + transcriptome + " " + "out=" + outputfilename_sam + " " + "ref=" + "dataflow/01-nucl/" + file

    input_gff3 = "dataflow/01-gff3/" + outputfilename

    outputfilename_count = outputfilename_sam.split(".sam")[0] + ".txt"

    if os.path.exists(outputfilename_sam):

        os.system(command)

        command = "htseq-count -s no -t CDS -i ID --additional-attr=ID" + " " + outputfilename_sam + " " + input_gff3 + " > " + outputfilename_count

        os.system(command)
