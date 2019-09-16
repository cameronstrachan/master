# python libraries
import os, sys
import subprocess
import pandas as pd

from Bio import Entrez, SeqIO
Entrez.email = 'strachc@gmail.com'

def get_assembly_summary(id):
    """Get esummary for an entrez id"""
    from Bio import Entrez
    esummary_handle = Entrez.esummary(db="assembly", id=id, report="full")
    esummary_record = Entrez.read(esummary_handle)
    return esummary_record

def get_assemblies(term):

    from Bio import Entrez, SeqIO
    Entrez.email = 'strachc@gmail.com'

    handle = Entrez.esearch(db="assembly", term=term, retmax='100000')
    record = Entrez.read(handle)
    ids = record['IdList']
    print (f'found {len(ids)} ids')
    ftps = []

    for id in ids:
        #get summary
        summary = get_assembly_summary(id)
        ftp = summary['DocumentSummarySet']['DocumentSummary'][0]['FtpPath_RefSeq']

        if ftp != '':
            ftps.append(ftp)

    return ftps

test = get_assemblies('Listeria monocytogenes')

print(test)

#file= open('dataflow/test/Pseudomonas_aeruginosa.fasta', 'w')

#for acc in acc_nums:
#    handle = Entrez.efetch(db="assembly", id=acc, type='fasta')
#    record = handle.read()
#    file.write(record)
