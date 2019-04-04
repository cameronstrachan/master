import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

file_obj = sc.Fasta('rumen_genomes_resistance_genes.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('rumen_genomes_resistance_genes.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.runprodigal()

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"
indir = 'dataflow/01-nucl/'
blastdbdir = 'dataflow/02-blast-db/'
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
#file_obj.runmakeblastdb(dbtype='nucl')

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj = sc.Fasta(file, indir)
file_obj.setOutputLocation(blastdir)

outputfilename = "resistance_island_mapping_allvall_V2.txt"
blastdb = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj.setOutputName(outputfilename)
#file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=500, evalue=1e-3, num_threads = 60, max_hsps = 10)


file = "rumen_genomes.fasta"
indir = 'dataflow/01-nucl/'
blastdbdir = 'dataflow/02-blast-db/'

# blast resistance islands against all

file_obj = sc.Fasta(file, indir)
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
#file_obj.runmakeblastdb(dbtype='nucl')

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, indir)
file_obj.setOutputLocation(blastdir)

outputfilename = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen_all_genomes.txt"
blastdb = "rumen_genomes.fasta"

file_obj.setOutputName(outputfilename)
#file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=500, evalue=1e-3, num_threads = 60, max_hsps = 10)


# extract all rumen resistance islands

file = 'rumen_genomes.fasta'

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location
outputfilename = file.split(".f")[0] + '_extractedCONTIGs_all_rumen' + '.fasta'
file_obj.setOutputName(outputfilename)
file_obj.setOutputLocation('dataflow/01-nucl/')
#file_obj.extractORFs_gff3(gff3_table_loc = 'dataflow/00-meta/resistance_blast_hit_cotigs_all_rumen.csv')

files = ["resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta", "rumen_genomes_extractedCONTIGs_all_rumen.fasta"]

#sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/rumen_genomes_extractedCONTIGs_all.fasta', filenames=files)


file = "rumen_genomes_extractedCONTIGs_all.fasta"
indir = 'dataflow/01-nucl/'
blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, indir)
file_obj.setOutputLocation(blastdir)

outputfilename = "resistance_island_mapping2.txt"
blastdb = "rumen_genomes_resistance_genes.fasta"

file_obj.setOutputName(outputfilename)
#file_obj.runblast(blast='blastn', db=blastdb, dblocation=blastdbdir, max_target_seqs=10, evalue=1e-3, num_threads = 60, max_hsps = 5)


# all prots against all prots from island

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
file_obj.setOutputName(file)
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.runprodigal()

file = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"
indir = 'dataflow/01-nucl/'
blastdbdir = 'dataflow/02-blast-db/'

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
file_obj.runmakeblastdb(dbtype='prot')

blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputLocation(blastdir)

outputfilename = "resistance_island_all_v_all_prot.txt"
blastdb = "resistance_island_blast_hits_concatenated_extractedCONTIGs_3rumen.fasta"

file_obj.setOutputName(outputfilename)
#file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=100, evalue=1e-3, num_threads = 60, max_hsps = 1)

headerfile = 'dataflow/02-headers/'

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(headerfile)
headers = file_obj.fasta2headermap()
df = pd.DataFrame.from_dict(headers, orient="index")
df['file'] = file
df.to_csv(headerfile + file.split('.fa')[0] + '.csv')

# RibD comparison, is the rib D in the island more related to the duplicated gene
# in the rumen metagenomes as compared to those in the pathogens

files = ['4309689-submission.assembly_rename.fasta', '4309680-submission.assembly_rename.fasta', 'RUG782_rename.fasta', "resistance_island_blast_hits_concatenated.fasta"]

sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/genomes_4_ribD.fasta', filenames=files)

file_obj = sc.Fasta('genomes_4_ribD.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('genomes_4_ribD.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.runprodigal()

file = "genomes_4_ribD.fasta"
indir = 'dataflow/01-nucl/'
blastdbdir = 'dataflow/02-blast-db/'

file_obj = sc.Fasta(file, 'dataflow/01-prot/')
file_obj.setOutputName(file)
file_obj.setOutputLocation(blastdbdir)
#file_obj.runmakeblastdb(dbtype='prot')

blastdir = 'dataflow/02-blast/'

file_obj = sc.Fasta("ecoli_ribD.fasta", 'dataflow/01-prot/')
file_obj.setOutputLocation(blastdir)

outputfilename = "genomes_4_ribD.txt"
blastdb = "genomes_4_ribD.fasta"

file_obj.setOutputName(outputfilename)
#file_obj.runblast(blast='blastp', db=blastdb, dblocation=blastdbdir, max_target_seqs=5000, evalue=1e-3, num_threads = 60, max_hsps = 1)


genes_df = pd.read_csv('dataflow/00-meta/ribd_comparison.csv', low_memory=False)
genes = genes_df['sseqid'].tolist()

file_obj = sc.Fasta('genomes_4_ribD.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('genomes_4_ribD_seqs.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
file_obj.subsetfasta(seqlist = genes, headertag='ribD')
