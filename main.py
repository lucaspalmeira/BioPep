import sys
from Bio import SeqIO
from Alpha.Biopep import Peptide
from Alpha.Modelling import Modelling
from Alpha.Submit import Dock
from output import output
import dock_scraping as ds


def execute(y, email, task):
    output.generate(task)
    for i, sequence in enumerate(SeqIO.parse(y, 'fasta')):
        print(f'Reading sequence{i}: {sequence.seq}')
        if len(list(str(sequence.seq))) <= 30:
            # Step 1 - Search homologous
            search = Peptide(str(i), str(sequence.seq))
            search.createfasta()
            search.runblast()

            # Step 2 - Modelling
            modeller = Modelling(str(i), str(sequence.seq), 30)
            modeller.run_modelling()

            # Step 3 - Docking
            # dock = Dock(str(i), str(sequence.seq), email)
            # dock.submit()

        else:
            print('Sequence longer than 30 amino acids.\n')
            continue
        
    print('Complete counterpart search.')
    print('Complete molecular modeling of peptides.')

    # ds.start_scraping()

    output.clear()
    output.finish()

    # print('Complete molecular docking of peptides.')


if __name__ == '__main__':
    execute(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
