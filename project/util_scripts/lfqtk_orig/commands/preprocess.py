
import modules.utils as utils
import commands.check as command_check
import path_utils


COMBINE_DBS_COMMAND = 'cat {fastas}'
REFORMAT_JAR_COMMAND = 'java -jar {jarfile} {combined_fasta}'
MAKE_DECOYS = 'perl {decoy_script} {in_combined_fasta} {out_decoy_fasta}'


def perform_preprocessing(args):

    in_fastas = args.input.split(',')
    out_fasta = args.output

    combined_fasta_fp = '{}.incomplete.combined'.format(out_fasta)
    formatted_fasta_fp = '{}.incomplete.combined.out'.format(out_fasta)
    decoy_fasta_fp = '{}.incomplete.combined.out.decoy'.format(out_fasta)

    combine_orig_fastas_command = COMBINE_DBS_COMMAND.format(fastas=" ".join(in_fastas))

    # Default output path is original filename with '.out' suffix
    reformat_command = REFORMAT_JAR_COMMAND.format(jarfile='{}/{}'.format(path_utils.get_basedir(), args.reformat_jar),
                                                   combined_fasta=combined_fasta_fp)

    decoy_command = MAKE_DECOYS.format(decoy_script='{}/{}'.format(path_utils.get_basedir(), args.decoy_script),
                                       in_combined_fasta=formatted_fasta_fp,
                                       out_decoy_fasta=decoy_fasta_fp)

    combine_decoy_command = COMBINE_DBS_COMMAND.format(fastas='{} {}'.format(formatted_fasta_fp, decoy_fasta_fp))

    utils.run_command(combine_orig_fastas_command, stdout_path=combined_fasta_fp, verbose=True)
    utils.run_command(reformat_command, verbose=True)
    utils.run_command(decoy_command, verbose=True)
    utils.run_command(combine_decoy_command, stdout_path=out_fasta, verbose=True)

    command_check.check_data(combined_fasta_fp, out_fasta)
