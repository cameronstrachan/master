# python libraries
import os, sys
import subprocess

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

files = [f for f in os.listdir('dataflow/01-bam/') if f.endswith(".bam")]

for file in files:
    file_id = file.split('_')[1]
    file_prefix = file.split('.bam')[0]
    file_sorted = file_prefix + ".sorted.bam"
    fastq_sorted = file_prefix + ".sorted.fastq"

    command = 'samtools sort --threads 60 -n dataflow/01-bam/' + file + ' -o dataflow/01-bam/' + file_sorted
    #os.system(command)

    command = 'bedtools bamtofastq -i dataflow/01-bam/' + file_sorted + ' -fq dataflow/01-fastq/' + file_id + '_R1.fastq' + ' -fq2 dataflow/01-fastq/' + file_id + '_R2.fastq'
    #os.system(command)


#os.system('gzip dataflow/01-fastq/*fastq')

files = [f for f in os.listdir('dataflow/01-fastq/') if f.endswith("_R1.fastq.gz")]

for file in files:

    dir = 'dataflow/01-fastq/'

    file_prefix = file.split('_R1')[0]

    file_r1 = file_prefix + '_R1.fastq.gz'
    file_r2 = file_prefix + '_R2.fastq.gz'

    file_r1_out = file_prefix + '_trimmed_R1.fastq.gz'
    file_r2_out = file_prefix + '_trimmed_R2.fastq.gz'

    command = 'trimmomatic PE -threads 60 -phred33 ' + dir + file_r1 + ' ' + dir + file_r2 + ' ' + dir + file_r1_out + ' ' + dir + file_r2_out + ' ILLUMINACLIP:/home/strachan/master/rusitec_metagenomes/dataflow/00-meta/neb.fasta:2:30:10:2:keepBothReads LEADING:5 TRAILING:5 MINLEN:36'

    os.system(command)
