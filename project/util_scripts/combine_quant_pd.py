#!/usr/bin/env python3

import argparse
import sys
import pandas as pd


def main():
    
    args = parse_arguments()
    check_input()

    col_names = ['peptide', 'protein'] + [name.split('/')[-1].split('.')[0] for name in args.dfs]

    acc_df = get_acc_df(args.dfs)
    acc_df.columns = col_names
    acc_df.to_csv(args.out_fp, sep="\t", index=False)


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('--dfs', nargs='+', required=True)
    parser.add_argument('--out_fp', required=True)
    args = parser.parse_args()
    return args


def check_input():
    if len(sys.argv) < 3:
        print('Usage format: {} {} {}'.format(sys.argv[0], 'out_fp', 'df_fps'))
        sys.exit(1)


def get_acc_df(df_fps):

    acc_df = None
    for df_fp in df_fps: 
        add_df = pd.read_csv(df_fp, skiprows=2, sep="\t").loc[:, ['peptide', 'protein', 'abundance']]
    
        if acc_df is None:
            acc_df = add_df
        else:
            acc_df = acc_df.merge(add_df, on=['peptide', 'protein'])

    return acc_df


if __name__ == '__main__':
    main()

