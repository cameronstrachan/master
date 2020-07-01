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

#bwa index cyo1_nanopore.fasta

files = [f for f in os.listdir('.') if f.endswith(".fastq")]

for file in files:
    bam_file_sorted = file_prefix + ".sorted.bam"
    bam_file_sorted_mapped = file_prefix + ".sorted.mapped.bam"
    fastq_file_mapped = file_prefix + ".sorted.mapped.fastq"
    fasta_file_mapped = file_prefix + ".sorted.mapped.fasta"

    command = 'samtools view -@ 60 -b -F 4 ' + bam_file_sorted + ' > ' + bam_file_sorted_mapped
    #os.system(command)

    command = 'samtools fastq ' + bam_file_sorted_mapped + ' > fastq/' + fastq_file_mapped
    #os.system(command)

    command = 'samtools fasta ' + bam_file_sorted_mapped + ' > fasta/' + fasta_file_mapped
    #os.system(command)


# blast mapped reads

file_obj = sc.Fasta('cyo1_nanopore.fasta', 'fasta/')
file_obj.setOutputName('cyo1_nanopore.fasta')
file_obj.setOutputLocation('blastdb/')
file_obj.runmakeblastdb(dbtype='nucl')



file_obj = sc.Fasta('32740_1.sorted.mapped.fasta', 'fasta')
file_obj.setOutputLocation('blast_output')
file_obj.setOutputName("32740_1.sorted.mapped.cyo1.txt")
file_obj.runblast(blast='blastn', db='cyo1_nanopore.fasta', dblocation='blastdb/', max_target_seqs=10, evalue=1e-5, num_threads = 10)
