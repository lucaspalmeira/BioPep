FROM python:3.9.17-slim-bullseye

# define python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

# install system packages
RUN apt-get update && apt-get install -y ncbi-blast+ nano curl git wget unzip gnupg
RUN git config --global --add safe.directory /home/biopep

# install miniconda
ENV PATH="/root/miniconda/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /root/miniconda \
    && rm /tmp/miniconda.sh \
    && conda update conda \
    && conda config --set auto_activate_base false

# download the Chrome Browser
RUN CHROME_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb \
    && apt-get -y install ./google-chrome-stable_${CHROME_VERSION}-1_amd64.deb

# download the Chrome Driver
RUN CHROME_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip \
    http://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip

# unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port as an environment variable
ENV DISPLAY=:99

# download Protein Data Bank (PDB)
RUN wget https://ftp.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt.gz \
    && gzip -d pdb_seqres.txt.gz \
    && mkdir blastdb \
    && mv pdb_seqres.txt /blastdb/pdb_seqres.fasta

# make blastdb
RUN makeblastdb -in /blastdb/pdb_seqres.fasta -dbtype prot -out /blastdb/pdb_seqres

# setup workdir
WORKDIR /home/biopep
ADD . .
RUN chmod -R 777 .

# create environment
RUN conda create --name biopep-env --file conda-linux-64.lock \
    && eval "$(conda shell.bash hook)" \
    && conda activate biopep-env \
    && sed -i "s/license = r'XXXX'/import os/g" ${CONDA_PREFIX}/lib/modeller-10.4/modlib/modeller/config.py \
    && echo "license = os.environ.get('KEY_MODELLER')" >> ${CONDA_PREFIX}/lib/modeller-10.4/modlib/modeller/config.py \
    && poetry install   
