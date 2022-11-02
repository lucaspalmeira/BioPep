# coding: utf-8

import os
import wget
import urllib
from modeller import *
from modeller.automodel import *
from datetime import datetime
from output import output


class Modelling:
    def __init__(self, index, peptide, cutoff):
        self.index = index
        self.peptide = peptide
        self.cutoff = cutoff

    def run_modelling(self):
        path = f'output/{output.get()}'
        pep_path = f'{path}/modelling/pep{self.index}'
        with open(f'{pep_path}/pep{self.index}.csv', 'r') as file:
            line = file.readline().split(',')
            try:
                code_pdb = line[1]

                print(code_pdb, code_pdb[0:4], code_pdb[5:])
                x = line[4:]

                for y in x:
                    pident = y.replace('\n', '')
                    if float(pident) >= self.cutoff:
                        print(f'Homologous sequence found. Identity = {pident}\n')

                        with open(f'{pep_path}/pep{self.index}.ali', 'a') as writing:
                            writing.write(f'>P1;pep{self.index}\n')
                            writing.write(f'sequence:pep{self.index}:::::::0.00: 0.00\n')
                            writing.write(self.peptide + '*')

                        try:
                            link = f'https://files.rcsb.org/download/{code_pdb[0:4]}.pdb'
                            wget.download(link, pep_path)

                        except (urllib.error.HTTPError, urllib.error.URLError):
                            print('urllib.error.HTTPError: HTTP Error 404: Not Found.')
                            self.__writelog('pdb file not found (download: error 404), unmodeled', cod=code_pdb[0:4])

                    else:
                        self.__writelog('low identity, unmodeled', cod=code_pdb[0:4])
                        continue

                    if os.path.isfile(f'{pep_path}/{code_pdb[0:4]}.pdb'):
                        try:
                            print('PDB file found.\n')
                            env = Environ()
                            aln = Alignment(env)
                            pdb = f'{pep_path}/{code_pdb[0:4]}'
                            # file='1bdm'
                            mdl = Model(env, file=pdb, model_segment=(f'FIRST:{code_pdb[5]}', f'LAST:{code_pdb[5]}'))
                            pdb_chain = code_pdb[0:4] + code_pdb[5]
                            # file='1bdmA'
                            aln.append_model(mdl, align_codes=pdb_chain, atom_files=f'{pep_path}/{code_pdb[0:4]}.pdb')
                            file_ali = f'{pep_path}/pep{self.index}.ali'
                            # file='TvLDH.ali'
                            code_ali = f'pep{self.index}'
                            # align_codes='TvLDH'
                            aln.append(file=file_ali, align_codes=code_ali)
                            aln.align2d()
                            ali = f'{pep_path}/pep{self.index}-{pdb_chain}.ali'
                            # file='TvLDH-1bdmA.ali'
                            aln.write(file=ali, alignment_format='PIR')
                            pap = f'{pep_path}/pep{self.index}-{pdb_chain}.pap'
                            # file='TvLDH-1bdmA.pap'
                            aln.write(file=pap, alignment_format='PAP')

                            env = Environ()
                            a = AutoModel(env, alnfile=ali,
                                          knowns=pdb_chain, sequence=code_ali,
                                          assess_methods=(assess.DOPE,
                                                          # soap_protein_od.Scorer(),
                                                          assess.GA341))
                            a.starting_model = 1
                            a.ending_model = 1
                            a.make()

                            # Move the modelling output files to output folder
                            output_models = [x for x in a.outputs if x['failure'] is None]
                            for om in output_models:
                                os.rename(om['name'], pep_path + '/' + om['name'])

                            exts = ['D00000001', 'ini', 'rsr', 'sch', 'V99990001']
                            for ext in exts:
                                os.rename(f'pep{self.index}.{ext}', f'{pep_path}/pep{self.index}.{ext}')

                            self.__writelog('pdb file found, modeled', False)

                        except ModellerError:
                            print('modeller.ModellerError')
                            self.__writelog('pdb file found, unmodeled (ModellerError)', cod=code_pdb[0:4])
                            continue

                    else:
                        print('PDB file not found.')
                        self.__writelog('PDB file not found, unmodeled', False)
                        continue

            except IndexError:
                print('Homologous not found.')
                self.__writelog('Homologous not found, unmodeled', False)

    def __writelog(self, msg, show_code=True, cod=''):
        path = f'output/{output.get()}'
        cod = f'{cod},' if show_code else ''
        with open(f'{path}/out.log', 'a') as outfile:
            outfile.write(f'pep{self.index}, {self.peptide}, {cod} pident, {msg}, '
                          f'{datetime.today().strftime("%Y-%m-%d %H:%M")}\n')
