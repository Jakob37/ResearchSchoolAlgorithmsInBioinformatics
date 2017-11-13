#!/usr/bin/env python3

import argparse

import commands.preprocess
import commands.upload
import commands.check
import commands.proteios_quant_to_normalyzer as proteios_quant_to_normalyzer
import commands.annotate_from_db as annotate_from_db
import commands.generate_spikein as generate_spikein
import commands.generate_spikein_set as generate_spikein_set

import versions as v

author = 'Jakob Willforss (jakob.willforss@immun.lth.se)'
help_message = 'Author: {}\n Version: {}\n\n' \
               'Utilities for working with label free quantification.' \
    .format(author, v.main)


ANSIBLE_ADD_DB_TEMPLATE = 'ansible/add_database_template.yml'
ANSIBLE_CONF_TEMPLATE = 'ansible/ansible.cfg'
ANSIBLE_HOSTS_TEMPLATE = 'ansible/ansible_hosts'

REFORMAT_JAR = 'scripts/ReformatFasta.jar'
DECOY_SCRIPT = 'scripts/decoy_new.pl'


def preprocess_data(args):

    commands.preprocess.perform_preprocessing(args)


def check_data(args):

    commands.check.check_data(args)


def upload_data(args):

    commands.upload.perform_ansible_upload(args)


def parse_arguments():

    parsers = ['db_process', 'db_check', 'db_upload_to_proteios', 'proteios_quant_to_normalyzer',
               'annotate_from_db', 'generate_spikein', 'generate_spikein_set']

    def default_func(args):
        print('Label Free Quantification ToolKit, version {}'.format(v.main))
        print('\n{}'.format('\n'.join(parsers)))
        exit(1)

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=default_func)

    subparsers = parser.add_subparsers(help='Commands: {}'.format(' '.join(parsers)))

    setup_db_process_parser(subparsers, parsers[0])
    setup_db_check_parser(subparsers, parsers[1])
    setup_db_upload_to_proteios_parser(subparsers, parsers[2])
    proteios_quant_to_normalyzer.setup_proteios_quant_to_normalyzer_parser(subparsers, parsers[3])
    annotate_from_db.setup_annotate_from_db(subparsers, parsers[4])
    generate_spikein.setup_simulation_parser(subparsers, parsers[5])
    generate_spikein_set.setup_simulation_parser(subparsers, parsers[6])

    args = parser.parse_args()
    args.func(args)


def setup_db_process_parser(subparsers, parser_name):

    parser = subparsers.add_parser(parser_name)
    parser.set_defaults(func=preprocess_data)

    parser.add_argument('-v', '--version', action='version', version=v.db_process)

    parser.add_argument('--input', help='Comma-delimited list of input files', required=True)
    parser.add_argument('--output', help='Path for final output', required=True)
    parser.add_argument('--reformat_jar', help='Name pre-processing jar', default=REFORMAT_JAR)
    parser.add_argument('--decoy_script', help='Decoy-generation script', default=DECOY_SCRIPT)


def setup_db_check_parser(subparsers, parser_name):

    parser = subparsers.add_parser(parser_name)
    parser.set_defaults(func=check_data)
    parser.add_argument('--input', help='Prepared database', required=True)


def setup_db_upload_to_proteios_parser(subparsers, parser_name):

    parser = subparsers.add_parser(parser_name)
    parser.set_defaults(func=upload_data)

    parser.add_argument('-v', '--version', action='version', version=v.upload_to_proteios)

    parser.add_argument('--file', help='Prepared database (absolute path)', required=True)
    parser.add_argument('--name', help='Name of database on server', required=True)
    parser.add_argument('--ansible_add_db_template', help='Ansible database upload template',
                        default=ANSIBLE_ADD_DB_TEMPLATE)
    parser.add_argument('--ansible_conf_template', help='Ansible conf template',
                        default=ANSIBLE_CONF_TEMPLATE)
    parser.add_argument('--ansible_hosts_template', help='Ansible hosts template',
                        default=ANSIBLE_HOSTS_TEMPLATE)


if __name__ == '__main__':
    parse_arguments()
