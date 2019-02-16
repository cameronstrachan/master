import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### RUN DIFFERENTIAL ABUNDANCE HENDERSON 2015
### Environment: source activate anaconda


genomes_df = pd.read_csv('dataflow/00-meta/prevotella_groupings.csv', low_memory=False)
genomes = genomes_df['file'].tolist()
files = [item + "_rename.fasta" for item in genomes]

sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/prevotella_groupings_genomes.fasta', filenames=files)

file_obj = sc.Fasta('prevotella_groupings_genomes.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('prevotella_groupings_genomes_db')
file_obj.setOutputLocation('dataflow/02-blast-db/')
file_obj.runmakeblastdb()

file_obj = sc.Fasta('lacto_signal_differential_all_seqs_tags.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('lacto_signal_differential_all_seqs_tags_grouped_prevotella_mapped')
file_obj.setOutputLocation('dataflow/03-blast-tables/')
file_obj.runblast(max_target_seqs=1, db='prevotella_groupings_genomes_db')
