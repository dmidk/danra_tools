import pandas as pd
import os
import sys
from rich.console import Console
from rich.table import Table
from rich import print
import subprocess

def call_grib_ls(gfile:str)-> list:
    cmd = "grib_ls -p name,shortName,paramId,level,levelType,date,time,step "+gfile
    try:
        ret=subprocess.check_output(cmd,shell=True)
        ret_clean=ret.decode("utf-8")
        lines=ret_clean.split("\n")
        messages=[i for i in lines if "messages" in i]
        nmsg=int(messages[0].split()[0])
        var_info = [i for i in lines if not any(y in i for y in ["messages","name",gfile])]
        var_info.pop()
        var_info.pop()
        clean_vars = [v.rstrip() for v in var_info]
        print(f"There are {nmsg} messages in {gfile}")
        return clean_vars
    except subprocess.CalledProcessError as err:
        print(f"subprocess error: {err}")
        #print(",".join([v.rstrip() for v in var_info]))


def format_rich_table( list_of_variables: list,
                      table_header:str,
                      print_table: bool,
                      print_summary_to_file: bool,
                      output_csv:str,
                      ) -> pd.DataFrame:
    """
    formats data from gribfile gfile
    in a rich table. 
    Returns dataframe and prints table on screen if requested
    """
    df_dict = {"name":[],"shortName":[],"paramId":[],"level":[],
            "levelType":[],"date":[],
            "time":[],"step":[]}
    table = Table(title=table_header) #f"All parameters in {gfile}")
    for col in df_dict.keys():
        table.add_column(col)
    for var in list_of_variables:
        split_all=var.split("  ") # use two spaces to differentiate between long names
        split_all = [x for x in split_all if x] # gets rid of all empty elements
        name = split_all[0]
        sname = split_all[1]
        parid = split_all[2]
        level = split_all[3]
        ltype = split_all[4]
        date = split_all[5]
        time = split_all[6]
        this_step = split_all[7] #step is a protected word in pdb
    
    #    level = split_all[-1]
        df_dict["name"].append(name)
        df_dict["shortName"].append(sname)
        df_dict["paramId"].append(parid)
        df_dict["level"].append(int(level))
        df_dict["levelType"].append(ltype)
        df_dict["date"].append(date)
        df_dict["time"].append(time)
        df_dict["step"].append(this_step)
        table.add_row(f"{name}",f"{sname}",f"{parid}",f"{level}",f"{ltype}",f"{date}",f"{time}",f"{this_step}")
    if print_table:    
        console=Console()
        console.print(table)
    df = pd.DataFrame(df_dict)

    if print_summary_to_file:
        print("Summary")
        if len(uniq_levels) > 1:
            uniq_levels.sort()
            clean_levels = [str(i) for i in uniq_levels]
            uniq_levels = ",".join(clean_levels)
        df_print = pd.DataFrame({"name":uniq_vars,"paramId":uniq_ids,"leveltype":uniq_ltype,"level":uniq_levels,"step":",".join(uniq_steps)})
        #print(df_print.to_markdown(index=False))
        #df_print.to_csv('sfc_only_fc_00.txt', mode='a', index=False, header=False,sep="|")
        df_print.to_csv(output_csv, mode='a+', index=False, header=False,sep=" ")
    return df

