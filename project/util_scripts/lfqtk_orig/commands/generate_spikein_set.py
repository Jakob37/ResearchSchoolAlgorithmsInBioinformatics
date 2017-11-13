from Bio import SeqIO
import numpy as np
import random
import sys

import versions as v

random.seed(0)


def setup_simulation_parser(subparsers, parser_name):

    parser = subparsers.add_parser(parser_name)

    parser.add_argument('-v', '--version', action='version', version=v.generate_spikein)

    parser.set_defaults(func=generate_spikein_set)

    parser.add_argument('--background_fa', help='', required=True)
    parser.add_argument('--spikein_fa', help='', required=True)
    parser.add_argument('--out_base', required=True)

    parser.add_argument('--offset_mean', default=0, type=float)
    parser.add_argument('--offset_std', default=0, type=float)

    parser.add_argument('--base_int', default=1000000, type=float)
    parser.add_argument('--noise_std', default=50000, type=float)
    parser.add_argument('--back_count', default=20, type=int)
    parser.add_argument('--spike_count', default=5, type=int)

    # parser.add_argument('--biological_var', default=0, type=float)
    parser.add_argument('--random_batch_effect', action='store_true')

    parser.add_argument('--spike_folds', help='Comma delimited', required=True)
    parser.add_argument('--offset_folds', help='Comma delimited')
    parser.add_argument('--sample_names', help='Comma delimited', required=True)

    parser.add_argument('--verbose', action='store_true')

    # parser.add_argument('--spike_int', default=1000000, type=int)
    # parser.add_argument('--spike_noise_std', default=50000, type=int)
    # parser.add_argument('--spike_count', default=20, type=int)


def generate_spikein_set(args):

    # Setup data and input check
    spike_folds = [float(fold) for fold in args.spike_folds.split(',')]

    if args.offset_folds is not None:
        offset_folds = [float(offset) for offset in args.offset_folds.split(',')]
    else:
        offset_folds = [0] * len(spike_folds)

    sample_names = args.sample_names.split(',')

    if len(spike_folds) != len(sample_names):
        print('Non-matching fold and name input: {} / {}'.format(args.spike_folds, args.sample_names))
        print('Aborting..')
        sys.exit(1)

    # Load data
    background = load_fasta(args.background_fa)
    spikein = load_fasta(args.spikein_fa)

    if args.verbose:
        print('{} entries loaded from {} as background'.format(len(background), args.background_fa))
        print('{} entries loaded from {} as spike-in'.format(len(spikein), args.spikein_fa))

    back_subset = pick_subset(background, args.back_count)
    spike_subset = pick_subset(spikein, args.spike_count)

    for sample_i in range(len(sample_names)):

        sample = sample_names[sample_i]
        spike_fold = spike_folds[sample_i]
        offset_fold = offset_folds[sample_i]

        assign_intensities(back_subset,
                           args.base_int,
                           args.noise_std,
                           bias_mean=args.offset_mean * offset_fold,
                           bias_std=args.offset_std)

        assign_intensities(spike_subset,
                           args.base_int * spike_fold,
                           args.noise_std,
                           bias_mean=args.offset_mean * offset_fold,
                           bias_std=args.offset_std)

        sample_subset = back_subset + spike_subset

        out_fp = '{}/{}'.format(args.out_base, sample)
        output_result(out_fp, sample_subset)

        if args.verbose:
            print('{} entries picked as background, {} as spike-in'.format(args.back_count, args.spike_count))
            print('{} entries written to {}'.format(len(sample_subset), out_fp))


def assign_intensities(fastas, intensity, noise_std, bias_mean, bias_std):

    base_int = np.random.normal(intensity, noise_std, len(fastas))

    if bias_mean != 0 or bias_std != 0:
        bias_int = np.random.normal(bias_mean, bias_std, len(fastas))
        total_int = base_int + bias_int
    else:
        total_int = base_int

    for i in range(len(fastas)):
        fa = fastas[i]
        intensity = total_int[i]
        quantity_str = '[# intensity={} #]'.format(intensity)
        fa.description = '{} {}'.format(fa.id, quantity_str)


def load_fasta(fasta_fp):

    fasta_ids = list()
    with open(fasta_fp) as in_fh:
        for record in SeqIO.parse(in_fh, 'fasta'):
            fasta_ids.append(record)
    return fasta_ids


def pick_subset(entries, pick_count):

    entry_sample = [entries[i] for i in sorted(random.sample(range(len(entries)), pick_count))]
    return entry_sample



def output_result(output_fa, fastas):

    with open(output_fa, 'w') as out_fh:
        SeqIO.write(fastas, out_fh, "fasta")
