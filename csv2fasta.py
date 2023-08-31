from tqdm import tqdm
import polars as pl
import os
import sys

def convert_to_fasta(file):
    df = pl.read_csv(file)
    filename = file.split("/")[-1]

    with open(f'{os.getcwd()}/{filename.split(".")[0]}.fasta', 'w') as fasta_file:
        for i in tqdm(range(len(df))):
            [row] = df[i,].rows(named=True)
            fasta_file.write(f'>{row["ID"]}')
            for key, value in row.items():
                if key not in ['Sequence', 'ID']:    
                    fasta_file.write(f'; {value}')
            fasta_file.write(f'\n{row["Sequence"]}\n')


def convert_to_multiple_fasta(file, folder):
    df = pl.read_csv(file)
    os.makedirs(folder)

    for i in tqdm(range(len(df))):
        [row] = df[i,].rows(named=True)
        pep_id = row["ID"]
        with open(f'{os.getcwd()}/{folder}/{pep_id}.fasta', 'w') as fasta_file:
            fasta_file.write(f'>{pep_id}')
            for key, value in row.items():
                if key not in ['Sequence', 'ID']:    
                    fasta_file.write(f'; {value}')
            fasta_file.write(f'\n{row["Sequence"]}\n')


if __name__ == '__main__':

    if len(sys.argv) == 3:
        convert_to_multiple_fasta(sys.argv[1], sys.argv[2])
    else:
        convert_to_fasta(sys.argv[1])