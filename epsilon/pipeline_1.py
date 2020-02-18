import os, sys
import subprocess

os.system("gtdbtk classify_wf --genome_dir dataflow/01-nucl --out_dir dataflow/02-classification --extension fa --cpus 60")
