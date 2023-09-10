import sys
from Bio import SeqIO
from Alpha.Biopep import Peptide
from Alpha.Modelling import Modelling
from Alpha.Submit import Dock
from output import output
import dock_scraping as ds
import os


# Constants
CUT_OFF = 30


def execute(query, task='task'):
    output.generate(task)
    for i, sequence in enumerate(SeqIO.parse(query, 'fasta')):
        print(f'Reading sequence{i}: {sequence.seq}')
        if len(list(str(sequence.seq))) <= CUT_OFF:
            # Step 1 - Search homologous
            search = Peptide(i, str(sequence.seq))
            search.createfasta()
            search.runblast()

            # Step 2 - Modelling
            modeller = Modelling(i, str(sequence.seq), CUT_OFF)
            modeller.run_modelling()

            # Step 3 - Docking
            dock = Dock(index=i,peptide= str(sequence.seq), receptor= f'{os.getcwd()}/input/receptor_6lzg.pdb', site= '455:B, 486:B, 493:B, 501:B, 505:B')
            dock.submit()

        else:
            print(f'Sequence longer than {CUT_OFF} amino acids.\n')
            continue
        
    print('Complete counterpart search.')
    print('Complete molecular modeling of peptides.')

    # Delete unmodeled peptides folders
    output.clear()

    # Get blast results
    print('Saving blast results...')
    output.blast()
    output.zip_pdbs()

    # Step 4 - Get docking results
    ds.start_scraping()

    print('Complete molecular docking of peptides.')

    output.finish()


if __name__ == '__main__':
    [_, query, task] = sys.argv
    execute(query, task)
