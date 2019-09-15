import os, sys
import subprocess
import pandas as pd

# custom libraries

system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

accession_list = ['SRX1334257', 'SRX1334308', 'SRX1334354', 'SRX1334200', 'SRX1334196', 'SRX1334196', 'SRX1334183', 'SRX6101286', 'SRX6101285', 'SRX6101284', 'SRX6101283', 'SRX6101282', 'SRX6101281', 'SRX6101280', 'SRX6101279', 'SRX6101278', 'SRX6101277', 'SRX6101276', 'SRX6101275', 'SRX6101274', 'SRX6101273', 'SRX6101272', 'SRX6101271', 'SRX6101270', 'SRX6101269', 'SRX6101268', 'SRX6101267', 'SRX6101266', 'SRX6101265', 'SRX6101264', 'SRX6101263', 'SRX6101262', 'SRX6101261', 'SRX6101260', 'SRX6101259', 'SRX6101258', 'SRX6101257', 'SRX6101256', 'SRX6101255', "SRX5053805", "SRX5053780", "SRX1607311", "SRX1607310", "SRX1607309", "SRX1607307", "SRX1607306", "SRX1607305", "SRX744081", "SRX744080", "SRX744079", "SRX744078", "SRX744077", "SRX744076", "SRX744075", "SRX744074", "SRX744073", "SRX744072", "SRX744071", "SRX744070", "SRX744069"]

for acc in accession_list:
    ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq')