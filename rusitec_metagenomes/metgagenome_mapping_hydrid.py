# python libraries
import os, sys
import subprocess

# custom libraries
system = str(input('\n' + 'Local or Server (L or S):'))

if system == 'S':
    sys.path.insert(0, '/home/strachan/master/')
else:
    sys.path.insert(0, '/Users/cameronstrachan/master/')

#bwa index dataflow/04-hybridassembly/SAMPLE_contigs.fasta
#bwa index dataflow/04-hybridassembly/114495_contigs.fasta

files = [f for f in os.listdir('dataflow/01-fastq/') if f.endswith("_trimmed_R1.fastq.gz")]
contig_files = [f for f in os.listdir('dataflow/04-hybridassembly/') if f.endswith(".fasta")]

for file in files:

    file_prefix = file.split('_trimmed_R1.fastq.gz')[0]

    file_r1 = file_prefix + '_trimmed_R1.fastq.gz'
    file_r2 = file_prefix + '_trimmed_R2.fastq.gz'

    for contig_file in contig_files:

        contig_file_prefix = contig_file.split('.fasta')[0]

        sam_file = file_prefix + '_' + contig_file_prefix + '_hybridassembly' + ".sam"
        command = "bwa mem -t 60 dataflow/04-hybridassembly/" + contig_file + " " + 'dataflow/01-fastq/' + file_r1  + ' dataflow/01-fastq/' + file_r2  + " > " + "../../../../proj/manngroup/strachan/tmp/" + sam_file

        if os.path.exists("../../../../proj/manngroup/strachan/tmp/" + sam_file):
            print('file exists: ' + sam_file)
        else:
            os.system(command)

        bam_file = file_prefix + '_' + contig_file_prefix + '_hybridassembly' + ".bam"
        command = "samtools view -@ 60 -bS " + "../../../../proj/manngroup/strachan/tmp/" + sam_file + " > " + "../../../../proj/manngroup/strachan/tmp/" + bam_file

        if os.path.exists("../../../../proj/manngroup/strachan/tmp/" + bam_file):
            print('file exists: ' + bam_file)
        else:
            os.system(command)

        bam_file_sorted = file_prefix + '_' + contig_file_prefix + '_hybridassembly' + ".sorted.bam"
        command = "samtools sort -@ 60 " + "../../../../proj/manngroup/strachan/tmp/" + sam_file + " > " + "../../../../proj/manngroup/strachan/tmp/" + bam_file_sorted

        if os.path.exists("../../../../proj/manngroup/strachan/tmp/" + bam_file_sorted):
            print('file exists: ' + bam_file_sorted)
        else:
            os.system(command)


#command = 'jgi_summarize_bam_contig_depths --outputDepth dataflow/04-tables/megahit-metagenome-depth.txt dataflow/03-alignments/*sorted.bam'
#os.system(command)

#command = 'metabat2 -i dataflow/04-coassembly/final.contigs.fa -a dataflow/04-tables/megahit-metagenome-depth.txt -o dataflow/04-bins/bin -m 1500 -t 70 -v --unbinned'
#os.system(command)
