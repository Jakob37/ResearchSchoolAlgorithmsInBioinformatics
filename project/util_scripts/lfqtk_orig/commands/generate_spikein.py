from Bio import SeqIO
import numpy as np
import random
import sys

import versions as v


def setup_simulation_parser(subparsers, parser_name):

    parser = subparsers.add_parser(parser_name)

    parser.add_argument('-v', '--version', action='version', version=v.generate_spikein)

    parser.set_defaults(func=generate_spikein)

    parser.add_argument('--background_fa', help='', required=True)
    parser.add_argument('--spikein_fa', help='', required=True)
    parser.add_argument('--output_fa', help='', required=True)

    parser.add_argument('--offset_mean', default=0, type=int)
    parser.add_argument('--offset_std', default=0, type=int)

    parser.add_argument('--back_int', default=1000000, type=int)
    parser.add_argument('--back_noise_std', default=50000, type=int)
    parser.add_argument('--back_count', default=500, type=int)

    parser.add_argument('--spike_int', default=1000000, type=int)
    parser.add_argument('--spike_noise_std', default=50000, type=int)
    parser.add_argument('--spike_count', default=20, type=int)

    parser.add_argument('--verbose', action='store_true')


def generate_spikein(args):

    background = load_fasta(args.background_fa)
    spikein = load_fasta(args.spikein_fa)

    if args.verbose:
        print('{} entries loaded from {} as background'.format(len(background), args.background_fa))
        print('{} entries loaded from {} as spike-in'.format(len(spikein), args.spikein_fa))

    assign_intensities(background, args.back_int, args.back_noise_std)
    assign_intensities(spikein, args.spike_int, args.spike_noise_std)

    picked_subset = pick_subset(background, spikein, args.back_count, args.spike_count)
    output_result(args.output_fa, picked_subset)

    if args.verbose:
        print('{} entries picked as background, {} as spike-in'.format(args.back_count, args.spike_count))
        print('{} entries written to {}'.format(len(picked_subset), args.output_fa))


def assign_intensities(fastas, intensity, noise_std, bias_mean=0, bias_std=0):

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


def pick_subset(background, spikein, back_count, spike_count):

    background_sample = [background[i] for i in sorted(random.sample(range(len(background)), back_count))]
    spike_sample = [spikein[i] for i in sorted(random.sample(range(len(spikein)), spike_count))]

    return background_sample + spike_sample


def output_result(output_fa, fastas):

    with open(output_fa, 'w') as out_fh:
        SeqIO.write(fastas, out_fh, "fasta")
