

import subprocess


def run_command(command, stdout_path=None, verbose=False):

    """Wrapper for running command line prompts"""

    if verbose:
        print("Running command: {command}, stdout: {stdout}".format(command=command, stdout=stdout_path))

    if not stdout_path:
        subprocess.call(command.split(' '))
    else:
        with open(stdout_path, 'w') as out_fh:
            subprocess.call(command.split(' '), stdout=out_fh)
