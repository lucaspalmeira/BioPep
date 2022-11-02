# coding: utf-8

import os
from Bio.Blast.Applications import NcbiblastpCommandline

from output import output


class Peptide:
    def __init__(self, index, peptide):
        self.index = index
        self.peptide = peptide

    def createfasta(self):
        pep_path = f'output/{output.get()}/modelling/pep{self.index}'
        os.makedirs(pep_path)
        with open(f'{pep_path}/pep{self.index}.fasta', 'a') as writing:
            writing.write('>pep' + self.index + '\n')
            writing.write(self.peptide)

    def runblast(self):
        pep_path = f'output/{output.get()}/modelling/pep{self.index}'
        command_blastp = NcbiblastpCommandline(task='blastp-short',
                                               query=f'{pep_path}/pep{self.index}.fasta',
                                               db=f'{os.getcwd() + "/pdb/pdb_seqres"}',
                                               outfmt='"10 qseqid sseqid evalue bitscore pident"',
                                               out=f'{pep_path}/pep{self.index}.csv')
        stdout, stderr = command_blastp()
