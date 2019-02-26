import os, sys
import pandas as pd

df_meta = pd.read_csv('dataflow/00-meta/sample-metadata.tsv', sep = '\t')
columns = list(df_meta)
columns.remove('#SampleID')
print(columns)
