#! /usr/bin/python3.8
# coding: utf-8

import sys
from Bio import SeqIO
from Alpha.Biopep import Peptide
from Alpha.Modelling import Modelling
from Alpha.Submit import Dock
from output import output


def execute(y, email, task):
    output.generate(task)
    for i, sequence in enumerate(SeqIO.parse(y, 'fasta')):
        print(f'Reading sequence{i}: {sequence.seq}')
        if len(list(str(sequence.seq))) <= 30:
            search = Peptide(str(i), str(sequence.seq))
            search.createfasta()
            search.runblast()
            modeller = Modelling(str(i), str(sequence.seq), 30)
            modeller.run_modelling()
            dock = Dock(str(i), str(sequence.seq), email)
            dock.submit()

        else:
            print('Sequence longer than 30 amino acids.\n')
            continue
    print('Complete counterpart search.')
    print('Complete molecular modeling of peptides.')
    print('The peptides were subjected to molecular docking, \
    after receiving all the emails with the results, \
    run the notebook to perform the data scraping.')

    output.clear()
    output.finish()


if __name__ == '__main__':
    execute(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
