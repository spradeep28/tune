#!/usr/bin/env python
# Copyright (c) 2014, Intel Corporation.

import sys, os
from argparse import ArgumentParser
import pandas as pd

def build_argparser():

    usage = '''example:
     python inter_results.py -i '/path/to/root/dir generated by launch.sh i.e. ~/tune/output/default/' 
     -o <optional: path to output dir to save summary_results.csv>
     '''

    parser = ArgumentParser(prog='launch_results_parser.py',
                            description='Intermediate benchmark results',
                            epilog=usage)
    args = parser.add_argument_group('Options')
    args.add_argument('-i', '--input_dir', help='Path to root directory of csv files with model performance data', required=True)
    args.add_argument('-o', '--output_dir', help='Output results directory', required=False, type=str, default='plot_results')

    return parser

def main():
    
    args = build_argparser().parse_args()

    ## Check if the results directory exists
    if not os.path.isdir(args.input_dir):
        print("Error: Invalid root directory")
        return -1
    else:
        root_path = args.input_dir

    ## Creating a new output directory 
    ## if user provided output directory doesn't exist
    if args.output_dir is not None: 
        if not os.path.isdir(args.output_dir):
            print(f"The specified output directory: {args.output_dir} doesn't exist! - Creating a new directory")
            os.makedirs(args.output_dir)

    ## Creating model specific results dataframes by parsing perf results csv
    data_frames = {}
    for curr_dir, list_dirs, file_names in os.walk(root_path):        
        for f in file_names:
            f_ext = os.path.splitext(f)[-1].lower()
            if f_ext == ".csv":
                fn = f.split('-')
                saved_fn = '_'.join(st for st in fn[1:-1])
                f_csv = os.path.join(curr_dir, f)
                df_csv = pd.read_csv(f_csv)
                if saved_fn in data_frames:
                    data_frames[saved_fn] = data_frames[saved_fn].append(df_csv)
                else:
                    data_frames[saved_fn] = df_csv
    
    ## Save results in the output directory
    for saved_fn, val_df in data_frames.items():
        print(f'Saving {saved_fn} profiling results')
        val_df.to_csv(os.path.join(args.output_dir, str(saved_fn)+".csv"), encoding='utf-8', index=False)
    
    print(f"Results parsed and available in directory: {args.output_dir}")

if __name__ == '__main__':
    sys.exit(main() or 0)
