import os, sys
import subprocess

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

genome_dir = '../cnoahi_phylogeny/concatenated_marker/complete_genomes/'

files = [f for f in os.listdir(genome_dir) if f.endswith(".fna")]
outdir = 'related_genomes/prokka/'

for file in files:

    file_prefix = file.split(".f")[0]
    command = 'prokka --outdir ' + outdir + file_prefix + ' --prefix ' + file_prefix + ' ' + genome_dir + file
    os.system(command)
