FROM python:3.9.17-slim-bullseye

# define python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

# install system packages
RUN apt update && apt install -y ncbi-blast+ nano curl git wget unzip gnupg
RUN git config --global --add safe.directory /home/biopep

# install miniconda
ENV PATH="/root/miniconda/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /root/miniconda \
    && rm /tmp/miniconda.sh \
    && conda update conda \
    && conda config --set auto_activate_base false

# adding trusting keys to apt for repositories
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmour -o /usr/share/keyrings/chrome-keyring.gpg 

# adding Google Chrome to the repositories
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google.list

# install package to download chrome
RUN apt update && apt install -y google-chrome-stable


# # download the Chrome Driver (OPTION 1)
# RUN CHROME_VERSION=$(google-chrome --product-version) && \
#     wget -O /tmp/chromedriver.zip \
#     http://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip
# # unzip the Chrome Driver into /usr/local/bin directory
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# download the Chrome Driver (OPTION 2)
RUN CHROME_VERSION=$(google-chrome --product-version) && \
    wget -O /tmp/chromedriver.zip \
    https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip
# unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/


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
ENV KEY_MODELLER=${KEY_MODELLER}
RUN conda create --name biopep-env --file conda-linux-64.lock \
    && eval "$(conda shell.bash hook)" \
    && conda activate biopep-env \
    && sed -i "s/license = r'XXXX'/import os/g" ${CONDA_PREFIX}/lib/modeller-10.4/modlib/modeller/config.py \
    && echo "license = os.environ.get('KEY_MODELLER')" >> ${CONDA_PREFIX}/lib/modeller-10.4/modlib/modeller/config.py \
    && poetry install   
