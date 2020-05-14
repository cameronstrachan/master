import subprocess
import re
import os

pathogens = ['mycobacterium tuberculosis', 'staphylococcus aureus', 'campylobacter coli', 'campylobacter jejuni', 'clostridioides difficile', 'acinetobacter baumannii', 'streptococcus pneumoniae', 'escherichia coli', 'pseudomonas aeruginosa', 'klebsiella pneumoniae', 'neisseria gonorrhoeae', 'streptococcus pyogenes']

df_folder = 'dataflow/01-dbs/pathogens/'

    for pathogen in pathogens:

        pathogen_string = '\'' + pathogen + '\''

        command = 'esearch -db assembly -query ' + pathogen + ' | esummary | xtract -pattern DocumentSummary -element FtpPath_GenBank'

        process = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        lines = output.splitlines()

        output_folder = df_folder + pathogen.replace(' ', '_') + '/'

        os.mkdir(output_folder)

        for line in lines:

            file_name = 'GCA_' + line.split('GCA_')[1] + '_genomic.fna.gz'
            ftp = line + '/' + file_name
            command = 'wget ' + ftp + ' -P ' + output_folder

            os.system(command)
