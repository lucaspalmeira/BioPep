#!/bin/bash

# Create flags
while getopts htf: flag; do
  case "${flag}" in
  t) compact=true ;;
  f) file=${OPTARG} ;;
  h | *)
    echo "usage: bash make.sh [-t] [-f <file-path>]"
    echo
    echo "options:"
    echo "  -f   Inform the file path"
    echo "  -t   Use this if the archive is zipped"
    echo
    echo "examples:"
    echo "  bash make.sh -tf pdb_seqres.fasta.tar.gz"
    echo "  bash make.sh -f pdb_seqres.fasta"
    exit
    ;;
  esac
done

# Exit the program if file parameter is not exists
if [ -z "$file" ]; then
  echo "error: inform the file path with -f option"
  echo "see help: \"bash make.sh -h\""
  exit 1
fi

# Verify if the file is compact
if [ $compact ]; then
  echo "Unzipping file..."
  tar -xzf "$file" -C pdb/
fi

# Create database
echo "Creating database..."
python3 pdb/make.py pdb/pdb_seqres.fasta

# Direct makeblastdb command
# makeblastdb -in pdb/pdb_seqres.fasta -dbtype prot -out pdb/pdb_seqres
