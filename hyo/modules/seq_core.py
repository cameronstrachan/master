#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import subprocess
import pandas as pd

'''
This is simply objects that define the different file formats I work with and the
associated methods for manipulating those files. The main object, from which all other inherit,
is simply defind as a file name and location. The main method from this object will be
to open the file.  This set of objects will be specific to sequence data.

'''

class File(object):

    '''
    File object defined by the name and location of the file. Only method is to open the file,
    which will be used by methods in sub classes. The print for this object will simply print
    the file name and location.
    '''

    def __init__(self, theName, theLocation, theOutputLocation='none', theOutputName='none'):

        self.name = theName
        self.location = theLocation
        self.outputlocation = theOutputLocation
        self.outputname = theOutputName

    # accesor methods (getters)
    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def getOutputLocation(self):
        return self.outputlocation

    def getOutputName(self):
        return self.outputname

    # mutator methods (setters)
    def setName(self, newName):
        self.name = newName

    def setLocation(self, newLocation):
        self.location = newLocation

    def setOutputLocation(self, newOutputLocation):
        self.outputlocation = newOutputLocation

    def setOutputName(self, newOutputName):
        self.outputname = newOutputName

    # print for object
    def __str__(self):
        return 'FILE[name=' + self.name + ', ' + 'location=' + self.location + ']'

    # open and close files
    def openfile(self):

        filepath = self.location + self.name

        try:
            infile = open(filepath,'r')
            return infile

        except IOError:
            print("\n" + 'File does not exist: ' + filepath)

    def openwritefile(self):
        outfilepath = self.outputlocation + self.outputname
        outfile = open(outfilepath, 'w')
        return outfile

    def outputexists(self):
        return os.path.exists(self.outputlocation + self.outputname)

class Fasta(File):

    '''
    There will be a object per type of file, which will have associated attributes for the
    manipulation of the file. The idea is that this class will just contain all the functions
    I write for manipulating fasta files. The first two functions will just create a dictionary
    of the sequence data for me to write further functions with. The next is simply one that creates
    a dictionary for mapping the headers. These dictionaries will be saved as attributes, but
    all just return the dictionary.
    '''

    def __init__(self, theName, theLocation):
        File.__init__(self, theName, theLocation)

        self.fastadict = {} # fasta file represented in a dictionary
        self.headers = {} # faata file headers represented in a mapping file


    def fasta2dict(self):

        '''
        This function takes a .fasta file input and returns a dictionary using the first
        part of the header (after the > and before the first white space) as the key
        and the full sequence as the value. This creates a convenient way to work with the
        sequences in python. The seqeuence dictionary gets assigned to a attribute called
        fastadict.
        '''



        infile = self.openfile()
        i = 1

        for line in infile:
            line = line.rstrip()

            if len(line) > 1:

                if line[0] == '>':
                    headersplit = line.split()
                    seqname = headersplit[0][1:]
                    self.fastadict[seqname] = ''
                    i = i + 1

                else:
                    self.fastadict[seqname] = self.fastadict[seqname] + line

        return self.fastadict



    def fasta2headermap(self):

        '''
        This function takes a .fasta file input and returns a dictionary using the first
        part of the header (after the > and before the first white space) as the key
        and the full header as the value. This creates a mapping file, so that the first
        part of the header can be used as a dictionary key, but then the entire header
        (assuming it contains useful information) can be mapped later. The mapping dictionary
        gets assigned to an attribute called headers.
        '''

        infile = self.openfile()

        for line in infile:
            line = line.rstrip()
            if line[0] == '>':
                headersplit = line.split()
                seqname = headersplit[0][1:]
                self.headers[seqname] = line
            else:
                pass

        return self.headers

    def saveonelinefasta(self, header='number'):

        '''
        Calling this function will simply save a new fasta file where all the sequences
        are on one line. This just cleans up the file in a way that makes it easier to work
        with. Most of the work I do though will be from the dictionary though.
        '''

        if not self.outputexists():
            fastadic = self.fasta2dict()
            outputfile = self.openwritefile()
            j = 1
            for k,v in fastadic.items():
                header = k.replace(':', '')
                seq = v.rstrip()
                if header == 'number':
                    outputfile.write(">" + header + '_' + str(j) + '\n')
                    outputfile.write(v + '\n')
                else:
                    outputfile.write(">" + header + '\n')
                    outputfile.write(v + '\n')
                j = j + 1
        else:
            print("\n" + 'File exists: ' + self.outputlocation + self.outputname)


    def subsetfasta(self, seqlist = []):

        '''

        '''


        if not self.outputexists():
            fastadic = self.fasta2dict()
            fastadic = {k: fastadic[k] for k in seqlist}
            outputfile = self.openwritefile()

            for k,v in fastadic.items():

                outputfile.write(">" + k + '\n')
                outputfile.write(v + '\n')

        else:
            print("\n" + 'File exists: ' + self.outputlocation + self.outputname)

    def headerrename(self):

        '''
        Number the sequences in each file and rename header with the file name and seq number.
        '''

        if not self.outputexists():
            fastadic = self.fasta2dict()
            outputfile = self.openwritefile()
            i = 1
            for k,v in fastadic.items():
                filename_nofasta = self.name.split('.f')[0]
                header = filename_nofasta + '_' + str(i)

                seq = v.rstrip()
                outputfile.write(">" + header + '\n')
                outputfile.write(v + '\n')

                i = i + 1
        else:
            print("\n" + 'File exists: ' + self.outputlocation + self.outputname)

    def lengthcutoff(self, replaceheaders = True, length = 500, direction = 'above'):
        '''
        Calling this function simply saves the files with a specific length cutoff
        in a folder called lengthcutoff.
        '''
        if not self.outputexists():
            fastadic = self.fasta2dict()
            outputfile = self.openwritefile()
            seqnum = 1
            filename_split = self.name.split('.f')

            for k,v in fastadic.items():
                header = k.rstrip()
                seq = v.rstrip()

                if direction == 'above':

                    if len(seq) >= length:
                        if replaceheaders == True:
                            outputfile.write(">" + str(filename_split[0]) + '_seq' + str(seqnum) + '\n')
                        else:
                            outputfile.write(">" + k + '\n')
                        outputfile.write(v + '\n')
                        seqnum = seqnum + 1


                else:

                    if len(seq) <= length:
                        if replaceheaders == True:
                            outputfile.write(">" + str(filename_split[0]) + '_seq' + str(seqnum) + '\n')
                        else:
                            outputfile.write(">" + k + '\n')
                        outputfile.write(v + '\n')
                        seqnum = seqnum + 1


        else:
            print("\n" + 'File exists: ' + self.outputlocation + self.outputname)

    def runprodigal(self, type = 'prot', gff3 = False):
        '''
        Run prodigal with the meta option. Need to create an option to change the prodigal paramaters
        '''

        if not self.outputexists():
            indir = self.location
            outdir = self.outputlocation
            filename = self.name
            fileoutputname = self.outputname

            if gff3 == False:
                if type == 'prot':
                    command = 'prodigal' + ' -i ' + indir + filename + ' -a ' + outdir + fileoutputname + ' -p ' + 'meta'
                else:
                    command = 'prodigal' + ' -i ' + indir + filename + ' -d ' + outdir + fileoutputname + ' -p ' + 'meta'
            else:
                command = 'prodigal' + ' -i ' + indir + filename + ' -f gff -o ' + outdir + fileoutputname + ' -p ' + 'meta'

            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        else:
            print("\n" + 'File exists: ' + self.outputlocation + self.outputname)

    def runmakeblastdb(self, dbtype='nucl'):
        '''
        Make local blast DB.
        '''
        indir = self.location
        outdir = self.outputlocation
        filename = self.name
        fileoutputname = self.outputname

        command = '../bin/makeblastdb'  + ' -in ' + indir + filename + ' -dbtype ' + dbtype + ' -out ' + outdir + fileoutputname
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    def runblast(self, blast='blastn', db='none', dblocation='dataflow/02-blast-db/', max_target_seqs=1, evalue=1e-3, num_threads = 8, max_hsps = 1):
        '''
        Run standalone blast
        '''

        if not self.outputexists():
            indir = self.location
            outdir = self.outputlocation
            filename = self.name
            fileoutputname = self.outputname

            command = '../bin/' + blast  + ' -query ' + indir + filename + ' -db ' + dblocation + db +  ' -max_target_seqs ' + str(max_target_seqs) + " -max_hsps " + str(max_hsps) + " -evalue " + str(evalue)  + ' -num_threads ' + str(num_threads) + " -outfmt '6 qseqid sseqid pident sstart send qstart qend evalue bitscore score qlen length sseq'" + ' -out ' + outdir + fileoutputname
            print('Blast command being run:' + '\n' + command)
            process = subprocess.Popen(command, universal_newlines=True, stdout=subprocess.PIPE, shell=True)
            output, error = process.communicate()
        else:
            print("\n" + 'File exists: ' + self.outputlocation + self.outputname)

# Testing program
def main():
    pass

if __name__ == '__main__':
    main()
