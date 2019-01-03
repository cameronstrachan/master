#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 09:33:21 2018

@author: cameronstrachan
"""

# python libraries
import os, sys
import pandas as pd

# custom libraries
sys.path.insert(0, '/Users/cameronstrachan/master/') 
from modules import seq_core as sc
from modules import seq_gen as sg
from modules import seq_scrape as ss

meta_df = pd.read_csv('dataflow/00-meta/seshadri2018_othergenomes.csv', low_memory=False)
strains = meta_df['genome'].tolist()

not_downloaded = list()
downloaded = list()

for strain in strains:
    message = ss.ncbigenomescrape(str(strain), searchterm2='genome[title]', location='dataflow/01-gb/')
    if message == 'No genomes downloaded':
        not_downloaded.append(strain)
    else:
        downloaded.append(strain)
        

