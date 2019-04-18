import os, sys
import subprocess
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqIO
import numpy as np
from Bio import SearchIO

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

# ant6 from ncbi

file_obj = sc.Fasta('ANT6_ncbi.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_ncbi_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'above')

file_obj = sc.Fasta('ANT6_ncbi_250.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_ncbi_250_350.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 350, direction = 'below')

# aph6 from ncbi

file_obj = sc.Fasta('APH3_ncbi.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_ncbi_200.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 200, direction = 'above')

file_obj = sc.Fasta('APH3_ncbi_200.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_ncbi_200_300.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 300, direction = 'below')

# sat4 from ncbi

file_obj = sc.Fasta('SAT4_ncbi.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('SAT4_ncbi_150.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 150, direction = 'above')

file_obj = sc.Fasta('SAT4_ncbi_150.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('SAT4_ncbi_150_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'below')


# ant6 from rumen

file_obj = sc.Fasta('ANT6_rumen.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_rumen_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'above')

file_obj = sc.Fasta('ANT6_rumen_250.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('ANT6_rumen_250_350.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 350, direction = 'below')

# aph6 from rumen

file_obj = sc.Fasta('APH3_rumen.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_rumen_200.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 200, direction = 'above')

file_obj = sc.Fasta('APH3_rumen_200.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('APH3_rumen_200_300.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 300, direction = 'below')

# sat4 from rumen

file_obj = sc.Fasta('SAT4_rumen.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('SAT4_rumen_150.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 150, direction = 'above')

file_obj = sc.Fasta('SAT4_rumen_150.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('SAT4_rumen_150_250.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.lengthcutoff(replaceheaders = False, length = 250, direction = 'below')


#../bin/muscle -in dataflow/01-prot/ANT6_ncbi_rumen_250_350_rename.fasta -out dataflow/03-alignments/ANT6_ncbi_rumen_250_350.afa -maxiters 3 -diags -sv -distance1 kbit20_3
#../bin/FastTree dataflow/03-alignments/ANT6_ncbi_rumen_250_350.afa > dataflow/03-trees/ANT6_ncbi_rumen_250_350.afa.newick

#../bin/muscle -in dataflow/01-prot/APH3_ncbi_rumen_200_300_rename.fasta -out dataflow/03-alignments/APH3_ncbi_rumen_200_300.afa -maxiters 3 -diags -sv -distance1 kbit20_3
#../bin/FastTree dataflow/03-alignments/APH3_ncbi_rumen_200_300.afa > dataflow/03-trees/APH3_ncbi_rumen_200_300.afa.newick

#../bin/muscle -in dataflow/01-prot/SAT4_ncbi_rumen_150_250_rename.fasta -out dataflow/03-alignments/SAT4_ncbi_rumen_150_250.afa -maxiters 3 -diags -sv -distance1 kbit20_3
#../bin/FastTree dataflow/03-alignments/SAT4_ncbi_rumen_150_250.afa > dataflow/03-trees/SAT4_ncbi_rumen_150_250.afa.newick

#../bin/muscle -in dataflow/01-prot/ANT6_ncbi_rumen_250_350_clade1.fasta -out dataflow/03-alignments/ANT6_ncbi_rumen_250_350_clade1.afa


file_obj = sc.Fasta('orfs_fig1_fig2.fasta', 'dataflow/01-prot/')
file_obj.setOutputName('orfs_fig1_fig2_rename.fasta')
file_obj.setOutputLocation('dataflow/01-prot/')
#file_obj.saveonelinefasta()



f = open("dataflow/02-blast/orfs_fig1_fig2_rename.txt", "r")
o = open("dataflow/02-blast/orfs_fig1_fig2_rename_parsed.txt", "w")

for x in f:
    if x.startswith('Query= '):
        o.write(x + '\n')

    if x.startswith('WP_'):
        o.write(x + '\n')
