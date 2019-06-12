import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg


file = "JQ655275.1.fasta"
blastdbdir = 'dataflow/02-blast-db/'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
#file_obj.runmakeblastdb(dbtype='nucl')


indir = 'dataflow/01-nucl/'
blastdir = 'dataflow/02-blast/'
file = "rumen_genomes.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdir)
outputfilename = "JQ655275_rumen_mapping.txt"
file_obj.setOutputName(outputfilename)

blastdb = "JQ655275.1.fasta"

file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=100, evalue=1e-3, num_threads = 60, max_hsps = 5)

file = "JQ655275.1.fasta"

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.runprodigal()


######

file = "orfs_fig1_fig2_rename.fasta"
blastdbdir = 'dataflow/02-blast-db/'

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
#file_obj.runmakeblastdb(dbtype='prot')


indir = 'dataflow/01-prot/'
blastdir = 'dataflow/02-blast/'
file = "orfs_fig1_fig2_rename.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdir)
outputfilename = "orfs_fig1_fig2_rename_mapping.txt"
file_obj.setOutputName(outputfilename)

blastdb = "orfs_fig1_fig2_rename.fasta"

#file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=100, evalue=1e-3, num_threads = 60, max_hsps = 1)

#######

file = "JQ655275.1.fasta"

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.runprodigal()



#### new tree using 2 versions of ANT6
####

file = "fig1_fig3_ncbi_nucl_hits.fasta"

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.runprodigal()

seqs_concatn = ['rumen_genomes.fasta', 'fig1_fig3_ncbi_nucl_hits.fasta']

sg.concat(inputfolder='dataflow/01-prot/', outputpath='dataflow/01-prot/pathogens_rumen.fasta', seqs_concatn):

file = "pathogens_rumen.fasta"
blastdbdir = 'dataflow/02-blast-db/'

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='prot')

indir = 'dataflow/01-prot/'
blastdir = 'dataflow/02-blast/'
file = "v1_v2_4309680.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdir)
outputfilename = "V1_V2_pathogens_rumen.txt"
file_obj.setOutputName(outputfilename)

blastdb = "pathogens_rumen.fasta.fasta"

file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=2000, evalue=1e-3, num_threads = 40, max_hsps = 1)
