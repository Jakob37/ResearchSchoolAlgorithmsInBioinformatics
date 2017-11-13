import pandas as pd

import versions as v


def setup_proteios_quant_to_normalyzer_parser(subparsers, parser_name):

    parser = subparsers.add_parser(parser_name)

    parser.add_argument('-v', '--version', action='version', version=v.proteios_quant_to_normalyzer)

    parser.set_defaults(func=convert_proteios_quant_to_normalyzer)
    parser.add_argument('--input', help='Proteios quantification matrix', required=True)
    parser.add_argument('--output', help='Prepared Normalyzer matrix', required=True)

    parser.add_argument('--nastr', help='String for NA values', default='NA')
    parser.add_argument('--rt_col', help='Optional column containing RT value, annotated as -1')
    parser.add_argument('--order_columns', action='store_true', help='Order columns on numeric value', default=False)


def convert_proteios_quant_to_normalyzer(args):

    in_fp = args.input
    out_fp = args.output

    header_df = pd.read_csv(in_fp, skiprows=4, sep='\t', dtype='str').head(4)
    data_df = pd.read_csv(in_fp, skiprows=9, sep='\t', na_values=args.nastr, header=None)

    annot_rows_df = get_annot_rows_df(header_df, rt_col=args.rt_col)
    parsed_data = get_parsed_data(data_df)

    final_df = annot_rows_df.append(parsed_data)

    if args.order_columns:
        # print(final_df.T.head())
        final_df = final_df.sort_values('a_sample_numbers', axis=1)

    final_df.to_csv(out_fp, header=False, index=False, sep='\t')
    print('Matrix with shape {} rows written to {}'.format(final_df.shape, out_fp))


def get_annot_rows_df(header_df, rt_col=None):

    filter_strings = ['Sample name']

    sample_names_w_na = header_df.iloc[0]
    annot_names_w_na = header_df.iloc[3]
    annot_names = list(annot_names_w_na.dropna())
    sample_names = [name for name in list(sample_names_w_na.dropna()) if name not in filter_strings]
    sample_levels = sorted(list(set(sample_names)))

    annot_numbers = [0] * len(annot_names)
    sample_numbers = [sample_levels.index(sample)+1 for sample in sample_names]

    if rt_col is not None:
        rt_i = annot_names.index(rt_col)
        annot_numbers[rt_i] = -1

    number_header = annot_numbers + sample_numbers
    annot_header = annot_names + sample_names
    annot_rows_df = pd.DataFrame({'a_sample_numbers': number_header, 'b_sample_annot': annot_header})

    return annot_rows_df.transpose()


def get_parsed_data(data_df, na_fill='NA'):

    return data_df.fillna(na_fill)















