# BioPep

> Pipeline for the search of homologues and molecular modeling for each peptide as well as the molecular docking between the peptides and the RBD receptor (PDB: 6LZG) of SARS-CoV-2.
>> By Lucas Palmeira: CNPq Technological Initiation Scholarship | Data Scientist in Training

## Licence
> GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

## Installation

Clone this repository:
```bash
git clone -b docker git@github.com:WilliamJSS/biopep.git
```

Navigate to project folder:
```bash
cd biopep
```

Copy .env file and add the `Modeller KEY`:
```bash
cp .env.example .env
```

Up containers:
```bash
docker compose up -d
```

## Run

Access BioPep container shell:
```bash
docker exec -it biopep bash
```

Activate conda environment:
```bash
eval "$(conda shell.bash hook)" && conda activate biopep-env
```

Execute BioPep:
```bash
python main.py query.fasta email@email.com taskname
```

`query.fasta`: file with peptides for submit <br>
`email@email.com`: your email address <br>
`taskname`: title to your task, for save in output folder

## Please, cite:
> ### BioPep
> Lucas Sousa Palmeira. (2021). BioPep. Zenodo. https://doi.org/10.5281/zenodo.5781778

> ### Hpepdock:
> ZHOU, Pei; JIN, Bowen; LI, Hao; et al. HPEPDOCK: A web server for blind peptide-protein acoplamento based on a hierarchical algorithm. Nucleic Acids Research, v. 46, n. W1, p. W443–W450, 2018.

> ### Modeller:
> ŠALI, Andrej; BLUNDELL, Tom L. Comparative protein modelling by satisfaction of spatial restraints. Journal of Molecular Biology, v. 234, n. 3, p. 779–815, 1993.
> 
> WEBB, Benjamin; SALI, Andrej. Comparative Protein Structure Modeling Using MODELLER. Current protocols in bioinformatics, v. 54, p. 5.6.1-5.6.37, 2016.

> ### Blast:
> CAMACHO, Christiam; COULOURIS, George; AVAGYAN, Vahram; et al. BLAST+: architecture and applications. BMC Bioinformatics, v. 10, p. 421, 2009.

> ### APD3: The antimicrobial peptide database
> WANG, Guangshun; LI, Xia; WANG, Zhe. APD3: The antimicrobial peptide database as a tool for research and education. Nucleic Acids Research, v. 44, n. D1, p. D1087–D1093, 2016.
