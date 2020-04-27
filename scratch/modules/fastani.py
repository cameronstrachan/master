#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import pandas as pd

def savefiles2list(filelist, filelocation, output):
    with open(output , 'w') as f:
        for item in filelist:
            file_write = filelocation + item
            f.write("%s\n" % file_write)

def allvall_fastani(filelist1, filelist2, threads=4, fragment_length=3000, extension=".fasta"):
    '''
    BLAH BLAH
    '''
    command = 'fastANI -t ' + str(threads) + ' --fragLen ' + str(fragment_length) + ' --ql ' + filelist1 + ' --rl ' + filelist2 + ' -o ' + 'ani.txt'
    print(command)
    os.system(command)

    df_output = pd.read_table('ani.txt', header = None)
    df_output = df_output.drop([3, 4], axis=1)
    df_output.columns = ['seq1', 'seq2', 'ani']

    df_output[['rm','seq1']] = df_output.seq1.str.split("/", expand=True)
    df_output["seq1"] = df_output.seq1.str.replace(extension, "")
    df_output[['rm','seq2']] = df_output.seq2.str.split("/", expand=True)
    df_output["seq2"] = df_output.seq2.str.replace(extension, "")
    df_output = df_output.drop(['rm'], axis=1)

    os.system('rm ani.txt')

    return(df_output)
