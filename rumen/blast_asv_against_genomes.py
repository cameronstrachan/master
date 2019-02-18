import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### RUN DIFFERENTIAL ABUNDANCE HENDERSON 2015
### Environment: source activate anaconda


#genomes_df = pd.read_csv('dataflow/00-meta/prevotella_groupings.csv', low_memory=False)
#genomes = genomes_df['file'].tolist()
#files = [item + "_rename.fasta" for item in genomes]

#sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/prevotella_groupings_genomes.fasta', filenames=files)

file_obj = sc.Fasta('prevotella_groupings_genomes_V3_V4.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('prevotella_groupings_genomes_V3_V4_db')
file_obj.setOutputLocation('dataflow/02-blast-db/')
file_obj.runmakeblastdb()

file_obj = sc.Fasta('sun2019-8_428-100.fasta', 'dataflow/01-nucl/')
file_obj.setOutputName('sun2019-8_428_prevotella_groupings_genomes_V3_V4_mapped')
file_obj.setOutputLocation('dataflow/03-blast-tables/')
file_obj.runblast(max_target_seqs=1, db='prevotella_groupings_genomes_V3_V4_db')

#perl ../bin/vxtractor/vxtractor.pl -h ../bin/vxtractor/HMMs/SSU/bacteria/ -r .V3-V4. -e 0.005 -i long -o dataflow/01-nucl/prevotella_groupings_genomes_V3_V4.fasta dataflow/01-nucl/prevotella_groupings_genomes.fasta
#perl ../bin/vxtractor/vxtractor.pl -h ../bin/vxtractor/HMMs/SSU/bacteria/ -r .V2-V3. -e 0.05 -i long -o dataflow/01-nucl/prevotella_groupings_genomes_V2_V3.fasta dataflow/01-nucl/prevotella_groupings_genomes.fasta
