# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

downloaddata = input("\n" + "Download data 3 Bioprojects? (y or n):")


if downloaddata == 'y':

    accession_list = ["SRX895490", "SRX895491", "SRX895493", "SRX895494", "SRX895496", "SRX895497", "SRX895499", "SRX895500", "SRX895502", "SRX895503", "SRX895506", "SRX895510", "SRX895512", "SRX895514", "SRX895516", "SRX895519", "SRX895524", "SRX895669", "SRX895672", "SRX1482723", "SRX1482749", "SRX1482750", "SRX1482752", "SRX1482753", "SRX1482754", "SRX1482755", "SRX1482756", "SRX902306", "SRX902307", "SRX902308", "SRX902309", "SRX902310", "SRX956405", "SRX956406", "SRX956407", "SRX956408", "SRX1182148", "SRX1182149", "SRX1182153"]


    for acc in accession_list:
        ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq')
