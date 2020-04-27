#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:19:31 2020

@author: cameronstrachan
"""

import pandas as pd
import numpy as np

# Functions
def splitvec(vector,distance) : 
    return list(map(list,np.split(vector,np.flatnonzero(np.diff(vector)>distance)+1)))



df = pd.read_csv('fragment_ani_1000.csv')

# Calculate SNP difference between fragment and genome average
# SNP difference must be equal or greater than 0

df_snp = df[df['genome1'] != df['genome2']]
df_snp.fragment_ani = df_snp.fragment_ani.round(1)
df_snp.genome_wide_ani = df_snp.genome_wide_ani.round(1)
df_snp = df_snp.assign(fragment_snps = (1 - (df_snp['fragment_ani']/100))*df_snp['fragment_size1']  )
df_snp = df_snp.assign(genome_wide_snps = (1 - (df_snp['genome_wide_ani']/100))*df_snp['fragment_size1']  )
df_snp = df_snp.assign(snp_diff = df_snp['genome_wide_snps'] - df_snp['fragment_snps'])
df_snp = df_snp[df_snp['snp_diff'] >= 0]

###

genomes1 = df_snp.genome1.unique()

list_df_regions = list()
    
for genome1 in genomes1:
    
    df_genome1 = df_snp[df_snp['genome1'] == genome1]
    genomes2 = df_genome1.genome2.unique()
    
    for genome2 in genomes2:
        
        df_single_comparison = df_genome1[df_genome1['genome2'] == genome2]
        df_single_comparison = df_single_comparison.sort_values(['snp_diff', 'fragment1'], ascending=[False, True])
        cont_regions = splitvec(df_single_comparison['fragment1'], 1)

        c = 1
        
        for region in cont_regions:
            # currently only for regions over 1, but i should remove this to look at 1kB regions at one point
            if len(region) > 1:
                df_region = pd.DataFrame(region, columns = ['fragment1'])
                df_region['n_continuous_frags'] = len(region)
                df_region['genome1'] = genome1
                df_region['genome2'] = genome2
                df_region['region_num'] = c
                
                list_df_regions.append(df_region)
                c = c + 1

df_regions = pd.merge(left=pd.concat(list_df_regions), right=df_snp, on=["genome1", "fragment1", "genome2"])

df_final_regions = df_regions[["genome1", "fragment1", "genome2", "region_num", "n_continuous_frags", 'fragment_snps', 'genome_wide_snps', 'snp_diff']]
df_final_regions.to_csv('fragment_ani_1000_regions.csv', index=False)