# python libraries
import os, sys
import subprocess
import pandas as pd

# custom libraries
sys.path.insert(0, '/home/strachan/master/')
from modules import seq_core_lin as sc
from modules import seq_gen_lin as sg
from modules import seq_scrape as ss

downloaddata = input("\n" + "Download data 3 Bioprojects? (y or n):")


if downloaddata == 'y':

    accession_list = ["SRX895490", "SRX895491", "SRX895493", "SRX895494", "SRX895496", "SRX895497", "SRX895499", "SRX895500", "SRX895502", "SRX895503", "SRX895506", "SRX895510", "SRX895512", "SRX895514", "SRX895516", "SRX895519", "SRX895524", "SRX895669", "SRX895672", "SRX1482723", "SRX1482749", "SRX1482750", "SRX1482752", "SRX1482753", "SRX1482754", "SRX1482755", "SRX1482756", "SRX902306", "SRX902307", "SRX902308", "SRX902309", "SRX902310", "SRX956405", "SRX956406", "SRX956407", "SRX956408", "SRX1182148", "SRX1182149", "SRX1182153"]


    for acc in accession_list:
        ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq/OMZ')



downloaddata = input("\n" + "Download data Luke et all? (y or n):")


if downloaddata == 'y':

    accession_list = ["SRX1337936", "SRX1337939"]


    for acc in accession_list:
        ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq/Luke')


downloaddata = input("\n" + "Download data Line P trial? (y or n):")


if downloaddata == 'y':

    accession_list = ["SRR3883063", "SRR3883064", "SRR3883065", "SRR3883066", "SRR3883067", "SRR3883179", "SRR3883180"]


    for acc in accession_list:
        ss.srafastqdownlaod(acc, outputdir='dataflow/01-fastq/LineP')




runprodigal = input("\n" + "Rename genomes and run prodigal on all nitrospina genomes to generate gff3 files? (y or n):")

if runprodigal == 'y':

    indir = 'dataflow/01-nucl/'
    files_all = [f for f in os.listdir(indir) if f.endswith(tuple([".fasta", ".fa", ".fna"]))]
    files = [ p for p in files_all if not(p.startswith('.'))]

    for file in files:

            file_obj = sc.Fasta(file, "dataflow/01-nucl/")

            outfilename = file.split('.f')[0] + '_rename.fasta'

            file_obj.setOutputName(outfilename)
            file_obj.setOutputLocation("dataflow/01-nucl/")

            file_obj.headerrename()

    files_r = [item.split('.f')[0] + "_rename.fasta" for item in files]

    sg.concat(inputfolder='dataflow/01-nucl/', outputpath='dataflow/01-nucl/all_nitrospina_genomes.fasta', filenames=files_r )

    file = "all_nitrospina_genomes.fasta"

    file_obj = sc.Fasta(file, 'dataflow/01-nucl/')
    # set output name, location
    outputfilename = file.split(".f")[0] + '.gff3'
    file_obj.setOutputName(outputfilename)
    file_obj.setOutputLocation('dataflow/01-prot/genes/')

    # run prodigal
    file_obj.runprodigal(gff3 = True)

    file_obj.setOutputName(file)
    file_obj.setOutputLocation('dataflow/01-prot/')

    file_obj.runprodigal()

runbowtie = input("\n" + "Run BBMap of 3 project transcriptomes against Nitrospina? (y or n):")

if runbowtie == 'y':

    indir = 'dataflow/01-fastq/OMZ'

    files_all = [f for f in os.listdir(indir) if f.endswith(".fastq")]
    files = [ p for p in files_all if not(p.startswith('.'))]

    for file in files:

        filename = file.split('_')[0]

        if file.split('_')[2] == '1.fastq':

            bbmap_command = "bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/" + \
            file + " " + "out=dataflow/03-sam/" + filename + "_all_nitrospina_genomes.sam" + \
            " ref=dataflow/01-nucl/all_nitrospina_genomes.fasta"

            print(bbmap_command)

            htseq_command = "htseq-count -s no -t CDS -i ID --additional-attr=ID " + \
            "dataflow/03-sam/" + filename + "_all_nitrospina_genomes.sam" + " " + \
            "dataflow/01-prot/genes/all_nitrospina_genomes.gff3 " + \
            "> " + "dataflow/03-sam-counts/" + filename + "_all_nitrospina_genomes.txt"

            print(htseq_command)

            os.system(bbmap_command)
            os.system(htseq_command)


runbowtie = input("\n" + "Run BBMap of Luke et al against Nitrospina? (y or n):")

if runbowtie == 'y':

    indir = 'dataflow/01-fastq/Luke'

    files_all = [f for f in os.listdir(indir) if f.endswith(".fastq")]
    files = [ p for p in files_all if not(p.startswith('.'))]

    for file in files:

        filename = file.split('_')[0]

        bbmap_command = "bbmap.sh threads=60 ambig=random in=dataflow/01-fastq/Luke/" + \
        file + " " + "out=dataflow/03-sam/" + filename + "_all_nitrospina_genomes.sam" + \
        " ref=dataflow/01-nucl/all_nitrospina_genomes.fasta"

        print(bbmap_command)

        htseq_command = "htseq-count -s no -t CDS -i ID --additional-attr=ID " + \
        "dataflow/03-sam/" + filename + "_all_nitrospina_genomes.sam" + " " + \
        "dataflow/01-prot/genes/all_nitrospina_genomes.gff3 " + \
        "> " + "dataflow/03-sam-counts/" + filename + "_all_nitrospina_genomes.txt"

        print(htseq_command)

        os.system(bbmap_command)
        os.system(htseq_command)
