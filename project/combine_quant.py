#!/usr/bin/env python3

import sys

sample_names = list()


class QuantEntry:

    def __init__(self, pep, prot, quant):
        self.pep = pep
        self.prot = prot
        self.quant = quant


def read_to_dict(fp):

    sample_dict = dict()
    with open(fp) as in_fh:
        for line in in_fh:
            line = line.rstrip()
            if line.startswith('#'):
                continue

            fields = [field.strip("\"") for field in line.split('\t')]
            pep = fields[0]
            sample_dict[pep] = QuantEntry(fields[0], fields[1], fields[3])
    return sample_dict


sample_dicts = dict()
for i in range(1, len(sys.argv)):

    sample_name = "s{}".format(i)
    sample_dicts[sample_name] = read_to_dict(sys.argv[i])


all_peps = set()
for d in sample_dicts.values():

    all_peps.update(set(d.keys()))

print(len(all_peps))

# for pep in all_peps:



















