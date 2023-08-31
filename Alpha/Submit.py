# coding: utf-8

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from output import output
from datetime import datetime

import time
import csv
import os


class Dock:
    def __init__(self, index, peptide, receptor, site):
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        self.driver = Chrome(options=options)
        self.peptide = peptide
        self.index = index
        self.receptor = receptor
        self.site = site

    def submit(self):
        path = f'{os.getcwd()}/output/{output.get()}'
        pep_path = f'{path}/modelling/pep{self.index}'
        ligand = f'{pep_path}/pep{self.index}.B99990001.pdb'
        if os.path.isfile(ligand):
            self.driver.get('http://huanglab.phys.hust.edu.cn/hpepdock/')

            # receptor protein file path and peptide file path
            self.driver.find_element(By.ID, 'pdbfile1').send_keys(self.receptor)
            self.driver.find_element(By.ID, 'pdbfile2').send_keys(ligand)
            
            # Advanced options
            self.driver.find_element(By.ID, 'option1').click()
            self.driver.find_element(By.NAME, 'sitenum1').send_keys(self.site)
            self.driver.find_element(By.NAME, 'jobname').send_keys(f'pep{self.index}')
            
            # submit docking
            self.driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[8]/td/input[1]').click()

            # the link is required to see future results
            time.sleep(5)
            link = self.driver.current_url

            exists_submit_file = os.path.exists(f'{path}/out_submit.csv')
            with open(f'{path}/out_submit.csv', 'a') as out_csv:
                csv_writer = csv.writer(out_csv, delimiter=',')
                if not exists_submit_file:
                    csv_writer.writerow(['Index', 'Sequence', 'Link'])
                csv_writer.writerow([self.index, self.peptide, link])

            self.driver.close()

        else:
            with open(f'{path}/submit.log', 'a') as log_csv:
                csv_writer = csv.writer(log_csv, delimiter=',')
                csv_writer.writerow([f'pep{self.index}.B99990001.pdb not found',
                                     f'{datetime.today().strftime("%Y-%m-%d %H:%M")}'])
            print('\nLigand not found.\n')

            self.driver.close()
