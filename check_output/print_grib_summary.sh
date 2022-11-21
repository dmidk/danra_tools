#!/bin/bash
eval "$(/data/users/cap/miniconda3/bin/conda shell.bash hook)"
conda activate py38
if [ -z $1 ]; then
   echo "Please provide one argument (file name)"
   echo "For more arguments, use print_codes.py outside script"
   echo "------------------------------------------"
   echo "Remember to load conda environment using:"
   echo "source ./utils.sh; load_conda"
   echo "Alternatively, use the py38.yml config to create your own conda environment"
   echo "------------------------------------------"

  ./print_codes.py -h
else
  ./print_codes.py -grib_file $1
fi

