# BioPep

> Pipeline for the search of homologues and molecular modeling for each peptide as well as the molecular docking between the peptides and the RBD receptor (PDB: 6LZG) of SARS-CoV-2.
>> By Lucas Palmeira: CNPq Technological Initiation Scholarship | Data Scientist in Training

## Licence
> GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

## Requisites

### Install Biopython
```
pip3 install biopython
```

### Download Protein Data Bank (PDB)
> Last updated: November 10, 2021 (183980 deposited crystallographic structures).
> 
> https://www.rcsb.org/downloads/fasta

### Create Data Base (PDB)
```
cd pdb/
```
```
tar -xvzf pdb_seqres.fasta.tar.gz
```
```
python3 make.py pdb_seqres.fasta
```

### Install Anaconda Python
```
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
```
```
bash Anaconda3-2021.11-Linux-x86_64.sh
```

### Install Modeller 10.1
```
conda install modeller
```
You will be prompted after installation to edit a file to add your Modeller license key.

### Install Geckodriver
Linux Ubuntu or CentOS 7
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz
```
```
tar -xvzf geckodriver-v0.30.0-linux32.tar.gz
```
```
chmod +x geckodriver
```
```
sudo mv geckodriver /usr/local/bin/
```

### Install Ncbi-Blast+ 

Linux Ubuntu
```
sudo apt install ncbi-blast+
```

Linux CentOS 7

```
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.12.0+-1.x86_64.rpm
```
```
sudo yum install ncbi-blast-2.12.0+-1.x86_64.rpm --nogpgcheck
```

## Run
```
python3 search.py file.fasta email@email.com
```

## Please, cite:
> ### BioPep
> Lucas Sousa Palmeira. (2021). BioPep. Zenodo. https://doi.org/10.5281/zenodo.5781778

> ### Hpepdock:
> ZHOU, Pei; JIN, Bowen; LI, Hao; et al. HPEPDOCK: A web server for blind peptide-protein acoplamento based on a hierarchical algorithm. Nucleic Acids Research, v. 46, n. W1, p. W443–W450, 2018.

> ### Modeller:
> ŠALI, Andrej; BLUNDELL, Tom L. Comparative protein modelling by satisfaction of spatial restraints. Journal of Molecular Biology, v. 234, n. 3, p. 779–815, 1993.
> WEBB, Benjamin; SALI, Andrej. Comparative Protein Structure Modeling Using MODELLER. Current protocols in bioinformatics, v. 54, p. 5.6.1-5.6.37, 2016.

> ### Blast:
> CAMACHO, Christiam; COULOURIS, George; AVAGYAN, Vahram; et al. BLAST+: architecture and applications. BMC Bioinformatics, v. 10, p. 421, 2009.

> ### APD3: The antimicrobial peptide database
> WANG, Guangshun; LI, Xia; WANG, Zhe. APD3: The antimicrobial peptide database as a tool for research and education. Nucleic Acids Research, v. 44, n. D1, p. D1087–D1093, 2016. Disponível em: </pmc/articles/PMC4702905/>. Acesso em: 26 nov. 2021.
