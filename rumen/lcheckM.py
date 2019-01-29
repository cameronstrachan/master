import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/') 
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg

### RUN checkM
### Environment: source activate py27

#checkm lineage_wf -t 60 -x fasta dataflow/01-checkmin dataflow/02-checkmout
#checkm qa dataflow/02-checkmout/lineage.ms dataflow/02-checkmout > dataflow/02-checkmout/qa_out.log

runcommand = input("\n" + "Run checkM pipeline? (y or n):")

if runcommand == 'y':
	os.system("checkm lineage_wf -t 60 -x fasta dataflow/01-checkmin dataflow/02-checkmout")
	os.system("checkm qa dataflow/02-checkmout/lineage.ms dataflow/02-checkmout > dataflow/02-checkmout/qa_out.log")


runcommand = input("\n" + "Clean up checkM results (also export a prevotella only table)? (y or n):")

if runcommand == 'y':
	os.system("Rscript src/R/checkM_summary.R")