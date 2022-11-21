#!/usr/bin/env python
"""
print the grib codes on the screen
If outfile given, then print output in a file
"""
import pandas as pd
import subprocess
import os
import sys
from rich.console import Console
from rich.table import Table
from rich import print
import format_output as fo
import tempfile

if __name__=="__main__":
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='''
            Example usage: ./print_codes.py -grib_file $FILE '''
            , formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-grib_file',help='grib file to process', type=str, default=None, required=True)
    #optional:
    parser.add_argument('-arxiv_path',help='Optional path for the archive files', type=str, default=None, required=False)
    parser.add_argument('-out_dir',help='Optional path for where to dump all the files in the tar ball', type=str, default=tempfile.mkdtemp(), required=False)
    parser.add_argument('-csv_file',help='Optional csv file for dumping all variables in csv file', type=str, default="all_vars.csv", required=False)
    parser.add_argument('-dump_tar_ball',action='store_true',help="Dump the all the files in tarball and print their contents in out_dir") #false by default. If given, extract

    args = parser.parse_args()
    gfile = args.grib_file
    out_dir = args.out_dir
    output_csv = args.csv_file
    dump_all = args.dump_tar_ball
    arxiv_dir = args.arxiv_dir

    if dump_all:
        #call tar zxvf 
        #gfiles = os.listdir(out_dir)
        print(f"Extract files in {arxiv_dir} to {out_dir}")
        print("Still to do")
        sys.exit(0)

    if gfile == "all":
        gfiles = os.listdir(out_dir)

    if len(sys.argv) == 3:
        outfile = sys.argv[2]
        print(f"Using output file {outfile}")
    #Testing options print some more info
    print_table=True #just for testing
    print_details = False
    print_mars_codes = False
    print_summary_to_file = False
    table_header=f"All parameters in {gfile}"
    if gfile == "all":
        for gf in gfiles:
            gfile = os.path.join(out_dir,gf)
            list_of_variables=fo.call_grib_ls(gfile)
            df= fo.format_rich_table(list_of_variables,
                                     table_header,
                                     print_table,
                                     print_summary_to_file,
                                     output_csv)
    else:        
        list_of_variables=fo.call_grib_ls(gfile)
        df= fo.format_rich_table(list_of_variables,
                                 table_header,
                                 print_table,
                                 print_summary_to_file,
                                 output_csv)




