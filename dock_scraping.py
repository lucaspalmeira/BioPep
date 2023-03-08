from selenium import webdriver
from selenium.webdriver.common.by import By

from output import output

import pandas as pd
import time
import wget
import os


def start_scraping():
    out_path = f'{os.getcwd()}/output/{output.get()}'
    df = pd.read_csv(f'{out_path}/out_submit.csv')

    items = items_copy = [{
        'Index': x['Index'], 'Link': x['Link'], 'Energy': 'NaN', 'Status': 'NONE'
    } for i, x in df.iterrows()]

    reloadtime = 120
    # Time to reload page, in seconds

    print('\nStarting docking scraping...')
    print(f'It\'s will try to do the docking scraping every {reloadtime} seconds.\n', flush=True)

    while len(items) > 0:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        for i, item in enumerate(items):
            driver.get(item['Link'])
            time.sleep(3)

            if 'is QUEUED' in driver.page_source:
                item['Status'] = 'QUEUED'
                continue
            elif 'is RUNNING' in driver.page_source:
                item['Status'] = 'RUNNING'
                continue
            else:
                item['Status'] = 'FINISHED'

            print('Collecting data...', item['Link'])
            element = driver.find_element(By.XPATH, '/html/body/center/table[3]/tbody/tr[2]/td[1]')
            item['Energy'] = element.text
            # Docking Score (1st model)

            dock_path = f'{out_path}/docking/pep{item["Index"]}'
            if not os.path.exists(dock_path):
                os.makedirs(dock_path)
            # Create docking results folder

            top10_models = f'{item["Link"]}top10_models.tar.gz'
            wget.download(top10_models)
            os.system(f'tar -xzf top10_models.tar.gz -C {dock_path}')
            # Download and extract files containing the 10 best positions of each peptide

            [directory] = os.listdir(dock_path)
            topmodels = os.listdir(f'{dock_path}/{directory}')
            for model in topmodels:
                os.rename(f'{dock_path}/{directory}/{model}', f'{dock_path}/{model}')
            os.rmdir(f'{dock_path}/{directory}')
            os.remove('top10_models.tar.gz')
            # Delete file and move models to pep folder

            print(f'Pep{item["Index"]} docking has completed. See top 10 models for it in:\n  {dock_path}\n')

        driver.close()

        items = [item for item in items if item['Energy'] == 'NaN']
        if len(items) > 0:
            print(f'Waiting docking... pep docks left: {len(items)}')
            print('  docks in queue:', len([k for k in items_copy if k['Status'] == 'QUEUED']))
            print('  docks running:', len([k for k in items_copy if k['Status'] == 'RUNNING']))
            print('  docks completed:', len([k for k in items_copy if k['Status'] == 'FINISHED']))
            print(flush=True)
            time.sleep(reloadtime)

    df['Energies'] = [item['Energy'] for item in items_copy]
    df.to_csv(f'{out_path}/results_dock.csv')


if __name__ == '__main__':
    start_scraping()
