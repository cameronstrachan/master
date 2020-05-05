#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# Functions
def splitvec(vector,distance) :
    return list(map(list,np.split(vector,np.flatnonzero(np.diff(vector)>distance)+1)))


# This is slow and needs to be parralized

def extract_continuous_regions(df_snp, distance=1, n_continuous=1, dir = 'decrease'):

    if  dir == 'decrease':
        df_snp = df_snp[df_snp['snp_diff'] >= 0]
    elif dir == 'increase':
        df_snp = df_snp[df_snp['snp_diff'] <= 0]
    else:
        pass

    genomes1 = df_snp.genome1.unique()

    list_df_regions = list()

    for genome1 in genomes1:

        df_genome1 = df_snp[df_snp['genome1'] == genome1]
        genomes2 = df_genome1.genome2.unique()

        for genome2 in genomes2:

            df_single_comparison = df_genome1[df_genome1['genome2'] == genome2]
            df_single_comparison = df_single_comparison.sort_values(['snp_diff', 'fragment1'], ascending=[False, True])
            cont_regions = splitvec(df_single_comparison['fragment1'], distance)

            for region in cont_regions:
                if len(region) >= n_continuous:
                    df_region = pd.DataFrame(region, columns = ['fragment1'])
                    df_region['n_continuous_frags'] = len(region)
                    df_region['genome1'] = genome1
                    df_region['genome2'] = genome2
                    list_df_regions.append(df_region)

    df_regions = pd.merge(left=pd.concat(list_df_regions), right=df_snp, on=["genome1", "fragment1", "genome2"])

    df_final_regions = df_regions[["genome1", "fragment1", "genome2", "n_continuous_frags", 'fragment_snps', 'genome_wide_snps', 'snp_diff']]

    return df_final_regions
