import os
import shutil
from datetime import datetime


# Start a task, generating an output folder with current datetime and task name
def generate(task: str):
    dt = datetime.today()
    directory = f'{dt.strftime("%Y.%m.%d-%H.%M.%S")}-{task}'
    path = f'{os.getcwd()}/output/{directory}'
    print(f'Generated output in: {path}')
    os.mkdir(path)

    # Write path in log file
    with open(f'{os.getcwd()}/output/outputs_history.log', 'a') as out_hist:
        line = f'{task}, started at = {dt.strftime("%Y-%m-%d %H:%M:%S")}, '
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
        out_hist.write(f'finished at = {dt.strftime("%Y-%m-%d %H:%M:%S")}\n')


# Delete unmodeled peptides folders
def clear():
    path = get()
    with open(f'{os.getcwd()}/output/{path}/out.log') as submit_log:
        lines = submit_log.readlines()
        for line in lines:
            items = line.split(', ')
            if 'unmodeled' in line:
                shutil.rmtree(f'{os.getcwd()}/output/{path}/modelling/{items[0]}')

