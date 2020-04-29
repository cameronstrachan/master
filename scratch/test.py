#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


sys.path.insert(0, '/Users/cameronstrachan/master/scratch/')
from modules import popani_core as pc


genome1_obj = pc.Fasta('GCF_000465235.1_ASM46523v1_major_contig.fasta', 'genomes/')

genome1_obj.setOutputLocation('test/')
genome1_obj.setOutputName('test.csv')
genome1_obj.split_up_genome_map(fragment_size=1000, step=100)
