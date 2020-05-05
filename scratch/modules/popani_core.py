#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

'''
BLAH BLAH
'''

class File(object):

    '''
	BLAH BLAH
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

    def deleteoutput(self):
        os.remove(self.outputlocation + self.outputname)

class Fasta(File):

    '''
    BLAH
    '''

    def __init__(self, theName, theLocation):
        File.__init__(self, theName, theLocation)

        self.fastadict = {} # fasta file represented in a dictionary
        self.headers = {} # fasta file headers represented in a mapping file


    def fasta2dict(self):

        '''
        BLAH BLAH
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

    def split_up_genome(self, fragment_size=1000, step=1000, write_to='multiple', return_map=True):

        '''
        BLAH BLAH
        '''

        if not self.outputexists():
            fastadic = self.fasta2dict()
            output_folder = self.outputlocation

            df_frament_locations = pd.DataFrame(columns=['header', 'contig', 'fragment1', 'start', 'stop', 'fragment_size', 'fragment_step'])

            for k,v in fastadic.items():

                header = k
                seq = v.rstrip()
                contig = 1

                start = 0
                end = fragment_size
                frag_num = 1

                while end < len(seq):

                    seq_fragment = seq[start:end]

                    if write_to == 'multiple':
                        file_name = str(frag_num) + '.fasta'
                        with open(output_folder + file_name, 'w') as f:
                            f.write('>' + header + '\n')
                            f.write(seq_fragment)

                        df_frament_locations = df_frament_locations.append({'header': header, 'contig': contig, 'fragment1':frag_num, 'start': start, 'stop': end, 'fragment_size': fragment_size, 'fragment_step': step}, ignore_index=True)

                    else:
                        output_file = self.openwritefile()
                        output_file.write(">" + header + '_' + str(contig) + '_' + str(frag_num) + '_' + str(start) + '_' + str(end) + '\n')
                        output_file.write(seq_fragment + '\n')

                        df_frament_locations = df_frament_locations.append({'header': header, 'contig': contig, 'fragment1':frag_num, 'start': start, 'stop': end, 'fragment_size': fragment_size, 'fragment_step': step}, ignore_index=True)

                    start = start + step
                    end = end + step
                    frag_num = frag_num + 1

                contig = contig + 1

            if return_map==True:
                return df_frament_locations

        else:
            print("\n" + 'Ouput file already exists: ' + self.outputlocation + self.outputname)
