import os, sys
import subprocess

os.system("checkm lineage_wf -t 60 -x fasta dataflow/01-nucl dataflow/02-checkmout")
os.system("checkm qa dataflow/02-checkmout/lineage.ms dataflow/02-checkmout > dataflow/02-checkmout/qa_out.log")
