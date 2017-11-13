ANSIBLE_COMMAND = "ansible-playbook {target_yml} --ask-become-sudo"


def perform_ansible_upload(args):

    prepare_ansible_files(args)
    # run_ansible()


def prepare_ansible_files(args):

    with open(args.ansible_add_db_template) as in_fh:
        add_database_template = in_fh.read()

    file_dir = '/'.join(args.file.split('/')[:-1])
    filename = args.file.split('/')[-1]

    replacements = dict()
    replacements['{DATABASE_FILENAME}'] = filename
    replacements['{DATABASE_NAME}'] = args.name

    updated_database_template = add_database_template

    for repl in replacements.keys():
        updated_database_template = updated_database_template.replace(repl, replacements[repl])

    ansible_path = '{}/add_database.yml'.format(file_dir)

    with open(ansible_path, 'w') as out_fh:
        print(updated_database_template, file=out_fh)

    print('Ansible upload playbook written to {}'.format(ansible_path))
    print('Perform upload by running:')
    print('> cd {}'.format(file_dir))
    print('> ansible-playbook {} --ask-become-pass'.format('add_database.yml'))
