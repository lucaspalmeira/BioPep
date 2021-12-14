# coding: utf-8

import os
import csv
from Bio.Blast.Applications import NcbiblastpCommandline


class Peptide:
    def __init__(self, index, peptide):
        self.index = index
        self.peptide = peptide

    def createfasta(self):
        with open(f'pep{self.index}.fasta', 'a') as writing:
            writing.write('>pep' + self.index + '\n')
            writing.write(self.peptide)

    def runblast(self):
        command_blastp = NcbiblastpCommandline(task='blastp-short', query=f'pep{self.index}.fasta',
                                               db=f'{os.getcwd() + "/pdb/pdb_seqres"}',
                                               outfmt='"10 qseqid sseqid evalue bitscore pident"',
                                               out=f'pep{self.index}.csv')
        stdout, stderr = command_blastp()