import os
import shutil
from datetime import datetime
import pandas as pd


# Start a task, generating an output folder with current datetime and task name
def generate(task: str):
    dt = datetime.today()
    log_file = f'{os.getcwd()}/output/outputs_history.log'
    directory = f'{dt.strftime("%Y.%m.%d-%H.%M.%S")}-{task}'
    path = f'{os.getcwd()}/output/{directory}'
    print(f'Generated output in: {path}')
    os.mkdir(path)

    endline = '\n' if os.path.isfile(log_file) else ''

    # Write path in log file
    with open(log_file, 'a') as out_hist:
        line = f'{endline}{task}, started at = {dt.strftime("%Y-%m-%d %H:%M:%S")}, finished at = '
        out_hist.write(line)

    return path


# Get all tasks output paths
def getall():
    outputs = []
    with open('output/outputs_history.log') as out_hist:
        lines = out_hist.readlines()
        for line in lines:
            [task, started_at, _] = line.split(', ')
            dt = datetime.fromisoformat(started_at[13:])
            out = f'{dt.strftime("%Y.%m.%d-%H.%M.%S")}-{task}'
            outputs.append(out)
    return outputs


# Get the more recent task output path
def get():
    outputs = getall()
    return outputs[-1]


# Set the task finish time
def finish():
    dt = datetime.today()
    with open(f'{os.getcwd()}/output/outputs_history.log', 'a') as out_hist:
        out_hist.write(dt.strftime("%Y-%m-%d %H:%M:%S"))


# Get peptides ids and sequences
def get_peptides(modelled=True):
    peptides = {}
    with open(f'{os.getcwd()}/output/{get()}/out.log') as submit_log:
        lines = submit_log.readlines()
        for line in lines:
            items = line.split(', ')
            if modelled and 'unmodeled' not in line:
                peptides[items[0]] = items[1]
            elif not modelled and 'unmodeled' in line:
                peptides[items[0]] = items[1]

    return peptides


# Delete unmodeled peptides folders
def clear():
    peptides = get_peptides(modelled=False)
    for pep in list(peptides.keys()):
        pep_folder = f'{os.getcwd()}/output/{get()}/modelling/{pep}'
        if os.path.exists(pep_folder):
            print(f'Excluding unmodeled peptide folder...\n  {pep_folder}\n')
            shutil.rmtree(pep_folder)


# Get blast results
def blast():
    output_task = f'{os.getcwd()}/output/{get()}'
    modelled_peptides = os.listdir(f'{output_task}/modelling')
    peptides = get_peptides()

    pep_dfs = []
    for pep in modelled_peptides:
        pep_dfs.append(pd.read_csv(f'{output_task}/modelling/{pep}/{pep}.csv', header=None))

    df = pd.concat(pep_dfs, ignore_index=True)
    df.columns = ['qseqid', 'sseqid', 'evalue', 'bitscore', 'pident', 'qseq', 'sseq', 'qcovs']

    sequences = []
    for i in range(len(df)):
        pep_id = df.iloc[i,0]
        sequences.append(peptides[pep_id])

    df = pd.concat([df, pd.Series(sequences, name='sequence')], axis=1)

    df = df.reindex(['qseqid', 'sseqid', 'sequence', 'evalue', 'bitscore', 'pident', 'qcovs', 'qseq', 'sseq'], axis=1)

    df.to_csv(f'{output_task}/blast.csv', index=False)


# Zip modeled pdb files
def zip_pdbs():
    output_task = f'./output/{get()}'
    peptides = get_peptides()

    os.makedirs('structures', exist_ok=True)

    for pep in list(peptides.keys()):
        pdb_file = f'{output_task}/modelling/{pep}/{pep}.B99990001.pdb'
        os.system(f'cp {pdb_file} structures/{pep}.pdb')

    os.system(f'tar -czvf {output_task}/structures.tar.gz structures')
    shutil.rmtree('structures')
