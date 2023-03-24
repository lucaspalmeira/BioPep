import os
import sys
from Bio.Blast.Applications import NcbimakeblastdbCommandline


def createdb(file):
    makeblastdb = NcbimakeblastdbCommandline(
        input_file=file,
        dbtype="prot",
        out=f'{os.getcwd()}/pdb/pdb_seqres'
    )
    makeblastdb()
    print('Database created successfully!')


if __name__ == '__main__':
    createdb(str(sys.argv[1]))
