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
outdir_16s = 'related_genomes/16s/'

for file in files:

    file_prefix = file.split(".f")[0]
    command = 'prokka --outdir ' + outdir + file_prefix + ' --prefix ' + file_prefix + ' ' + genome_dir + file
    #os.system(command)

    file_16s = open(outdir_16s + file_prefix + '.fasta', 'w')

    file_ffn = open(outdir + file_prefix + '/' + file_prefix + '.ffn', 'r')
    lines = file_ffn.readlines()

    line_count = 0
    for line in lines:
        line_count2 = line_count + 1
        line_count = line_count + 1
        if line[0] == '>':
            if '16S ribosomal RNA' in line:
                print(file)
                print(line)
                file_16s.write(line)
                while lines[line_count2][0] != '>':
                    file_16s.write(lines[line_count2])
                    line_count2 = line_count2 + 1

        else:
            pass
