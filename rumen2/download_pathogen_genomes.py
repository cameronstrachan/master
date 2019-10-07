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

def get_project_ids(term):

    from Bio import Entrez, SeqIO
    Entrez.email = 'strachc@gmail.com'

    handle = Entrez.esearch(db="assembly", term=term, retmax='100000')
    record = Entrez.read(handle)
    ids = record['IdList']
    numbers = dict()

    for id in ids:
        #get summary
        summary = get_assembly_summary(id)
        acessions = summary['DocumentSummarySet']['DocumentSummary'][0]['AssemblyAccession']
        project = summary['DocumentSummarySet']['DocumentSummary'][0]['GB_BioProjects'][0]['BioprojectAccn']
        numbers.update({acessions:project})
        import time
        #time.sleep(0.1)
    return numbers

project_ids = get_project_ids('clostridioides difficile')

def get_project_summary(id):
    """Get esummary for an entrez id"""
    from Bio import Entrez
    esummary_handle = Entrez.esummary(db="bioproject", id=id, report="full")
    esummary_record = Entrez.read(esummary_handle)
    print(esummary_record)
    return esummary_record

def get_projectinfo(term):
    from Bio import Entrez, SeqIO
    Entrez.email = 'strachc@gmail.com'

    handle = Entrez.esearch(db="bioproject", term=term, retmax='100000')
    record = Entrez.read(handle)
    id = record['IdList']
    summary = get_project_summary(id)
    title = summary['DocumentSummarySet']['DocumentSummary'][0]['Project_Title']
    description = summary['DocumentSummarySet']['DocumentSummary'][0]['Project_Description']
    rel_med = summary['DocumentSummarySet']['DocumentSummary'][0]['Relevance_Medical']
    rel_ag = summary['DocumentSummarySet']['DocumentSummary'][0]['Relevance_Agricultural']

    title_desc = title + " : " + description + " : " + rel_med + ' : ' + rel_ag
    return title_desc

descriptions = dict()

for k,v in project_ids.items():
    info = get_projectinfo(v)
    descriptions.update({k:info})

df = pd.DataFrame.from_dict(descriptions, orient="index")
df.to_csv('dataflow/03-analysis/cdiff_projects.csv')
