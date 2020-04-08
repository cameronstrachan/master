# python libraries
import os, sys
import subprocess
import pandas as pd
import re

df_rename = pd.read_csv('tree_rename.csv', low_memory=False)

for index, row in df_rename.iterrows():
    print(row['names'], row['rename'])

fh = open('01-nucl/alignment_233_2235_new3.fasta.treefile')
tree = fh.read()

for index, row in df_rename.iterrows():
    tree = tree.replace(str(row['names']), str(row['rename']))

oh = open('01-nucl/alignment_233_2235_new3.fasta.treefile'+'.rename.tree', 'w')
oh.write(tree)
oh.close()
