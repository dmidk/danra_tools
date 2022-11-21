#!/usr/bin/env bash
load_conda() {
	   eval "$(/data/users/cap/miniconda3/bin/conda shell.bash hook)"
	   conda activate py38
            }
export -f load_conda
