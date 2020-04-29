#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import pandas as pd

sys.path.insert(0, '/Users/cameronstrachan/master/scratch/')
from modules import popani_core as pc
from modules import fastani as fa
from modules import conservX as cx

df_final = pd.read_csv('popani_100_5.csv')

#df_snp = cx.calculate_snp_decrease_df(df_final, dec_places = decimals)
#df_final_regions = cx.extract_continuous_regions(df_snp, distance = dist)