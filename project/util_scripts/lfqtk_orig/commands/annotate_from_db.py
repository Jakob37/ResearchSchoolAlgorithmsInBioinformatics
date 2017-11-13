from Bio import SeqIO
import pandas as pd
import sys

import versions as v


def setup_annotate_from_db(subparsers, parser_name):

    parser = subparsers.add_parser(parser_name)

    parser.add_argument('-v', '--version', action='version', version=v.annotate_from_db)

    parser.set_defaults(func=main)
    parser.add_argument('--dbs', help='Database source fasta files, comma delimited', required=True)
    parser.add_argument('--db_labs', help='Labels to assign to db entries, comma delimited', required=True)
    parser.add_argument('--target', help='File in which to update IDs', required=True)
    parser.add_argument('--output', help='Output path', required=True)

    parser.add_argument('--target_col', help='Zero-indexed column with IDs to annotate', required=True, type=int)

    parser.add_argument('--delim', help='Optional delimitor for multiple IDs in one field')
    parser.add_argument('--filetype', help='Proteios quantification matrix', choices=['tsv'], default='tsv')

    parser.add_argument('--NOTDONERUNANYWAY', action='store_true', default=False)


def main(args):

    print('WARNING: IMPLEMENTATION NOT FULLY DONE AND TESTED!')
    if not args.NOTDONERUNANYWAY:
        print('Stopping, to force uncompleted run, use flag NOTDONERUNANYWAY')
        sys.exit(0)

    db_ids = read_databases(args.dbs.split(','), args.db_labs.split(','))

    if args.filetype == 'tsv':
        orig_df = pd.read_csv(args.target, sep='\t', header=None, na_filter=False)
        annot_df = get_updated_column_df(orig_df, db_ids, args.target_col)
        print('Writing Matrix with shape {} to {}'.format(annot_df.shape, args.output))
        annot_df.to_csv(sep='\t', header=False, index=False)
    else:
        raise ValueError('Filetype not implemented: {}'.format(args.filetype))


def read_databases(databases, labels):

    db_id_dict = dict()

    lab_i = 0
    for db in databases:

        curr_ids = list()

        print('THIS NEEDS TO BE GENERALIZED!')

        with open(db) as in_fh:
            for record in SeqIO.parse(in_fh, 'fasta'):
                # print(record.id.split('|')[1])
                curr_ids.append(record.id.split('|')[1])

        print('db: {} entries: {}'.format(labels[lab_i], len(curr_ids)))
        db_id_dict[labels[lab_i]] = curr_ids
        lab_i += 1

    return db_id_dict


def get_updated_column_df(df, db_dict, target_col):

    annot_df = df.copy()
    annot_col = list(df[target_col])

    missing = 0

    print(len(annot_col))

    for i in range(len(annot_col)):
        val = str(annot_col[i])

        if i % 1000 == 0:
            print(i)
            print(missing)

        for subval in val.split(','):

            matching_dbs = list()

            for db in db_dict:
                if subval in db_dict[db]:
                    matching_dbs.append(subval)
            if len(matching_dbs) != 1:
                missing += 1
                # print('{} is matching dbs: {}, skipping'.format(subval, matching_dbs))
            else:
                annot_col[i].replace(subval, '{}{}'.format(subval, matching_dbs[0]))

    print('Missing: {}'.format(missing))

    annot_df[target_col] = annot_col
    return annot_df


def output_target():
    pass
