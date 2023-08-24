FROM python:3.9.17-slim-bullseye

# define python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

# install system packages
RUN apt update && apt install -y ncbi-blast+ wget
# RUN apt update && apt install -y ncbi-blast+ curl git wget unzip gnupg
# RUN git config --global --add safe.directory /home/biopep

# # adding trusting keys to apt for repositories
# RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
#     | gpg --dearmour -o /usr/share/keyrings/chrome-keyring.gpg 

# # adding Google Chrome to the repositories
# RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
#     > /etc/apt/sources.list.d/google.list

# # install package to download chrome
# RUN apt update && apt install -y google-chrome-stable

# # download the Chrome Driver
# RUN CHROME_VERSION=$(google-chrome --product-version) && \
#     wget -O /tmp/chromedriver.zip \
#     http://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip

# # unzip the Chrome Driver into /usr/local/bin directory
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# alternative download...
# download the Chrome Driver
# RUN CHROME_VERSION=$(google-chrome --product-version) && \
#     wget -O /tmp/chromedriver.zip \
#     https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip

# unzip the Chrome Driver into /usr/local/bin directory
# RUN unzip /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/


# # set display port as an environment variable
# ENV DISPLAY=:99

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

# install poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -
# ENV PATH="/root/.local/bin:${PATH}"

# install project packages
# RUN poetry install
