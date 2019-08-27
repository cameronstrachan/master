# python libraries
import os, sys
import subprocess
import pandas as pd
import re

df_rename = pd.read_csv('tree_rename.csv', low_memory=False)

for index, row in df_rename.iterrows():
    print(row['names'], row['rename'])

fh = open('actinos_new_seqs_outlier_full_coverage.fasta.treefile')
tree = fh.read()

for index, row in df_rename.iterrows():
    tree = tree.replace(row['names'], row['rename'])

oh = open('actinos_new_seqs_outlier_full_coverage.fasta.treefile'+'.rename.tree', 'w')
oh.write(tree)
oh.close()
