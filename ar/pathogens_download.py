import subprocess
import re
import os


pathogens = ['staphylococcus aureus', 'campylobacter coli', 'campylobacter jejuni', 'clostridioides difficile', 'salmonella typhimurium', 'salmonella newport', 'staphylococcus pseudintermedius', 'streptococcus agalactiae', 'enterococcus faecium', 'erysipelothrix rhusiopathiae', 'streptococcus suis']

#others
#pathogens = ['mycobacterium tuberculosis', 'acinetobacter baumannii', 'streptococcus pneumoniae', 'escherichia coli', 'pseudomonas aeruginosa', 'klebsiella pneumoniae', 'neisseria gonorrhoeae', 'streptococcus pyogenes']


df_folder = 'dataflow/01-dbs/pathogens/'

downloadpathogens = input("\n" + "Download pathogen genomes? (y or n):")
#print('Current pathogen search terms: ' + pathogens)

if downloadpathogens == 'y':

    for pathogen in pathogens:

        pathogen_string = '\'' + pathogen + '\''

        command = 'esearch -db assembly -query ' + pathogen_string + ' | esummary | xtract -pattern DocumentSummary -element FtpPath_GenBank'

        process = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        lines = output.splitlines()

        output_folder = df_folder + pathogen.replace(' ', '_') + '/'

        if os.path.exists(output_folder) == False:
            os.mkdir(output_folder)

        for line in lines:

            file_name = 'GCA_' + line.split('GCA_')[1] + '_genomic.fna.gz'
            ftp = line + '/' + file_name
            command = 'wget ' + ftp + ' -P ' + output_folder

            os.system(command)
