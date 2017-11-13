from Bio import SeqIO


def check_data(orig_fasta, final_fasta):

    print("final fasta: {}".format(final_fasta))

    orig_recs = SeqIO.to_dict(SeqIO.parse(orig_fasta, "fasta"))
    final_recs = SeqIO.to_dict(SeqIO.parse(final_fasta, "fasta"))

    rec_count_err = check_record_counts(orig_recs, final_recs)
    decoy_count_err = check_decoy_counts_in_final(final_recs)
    decoy_sample_err = check_decoy_entry(final_recs)

    if not rec_count_err and not decoy_count_err and not decoy_sample_err:
        print("Everything is looking fine")
    else:
        print("ERRORS encountered while checking data - Make sure to take a closer look")


def check_record_counts(orig_recs, final_recs):

    orig_count = len(orig_recs)
    final_count = len(final_recs)

    print("Orig count: {}, final count: {}".format(orig_count, final_count))

    errors = False
    if 2 * orig_count != final_count:
        print("ERROR: Final count expected to be twice the original, this is not the case")
        errors = True

    return errors


def check_decoy_counts_in_final(final_recs):

    tot_count = 0
    r_count = 0

    for key in final_recs.keys():
        if key.startswith('r'):
            r_count += 1
        tot_count += 1

    print("In final database, tot count: {}, decoy count: {}".format(tot_count, r_count))

    errors = False
    if 2 * r_count != tot_count:
        print("ERROR: Half of entries in final database should be decoys, this is not the case")
        errors = True

    return errors


def check_decoy_entry(final_recs):

    entry_key = [rec for rec in final_recs.keys() if not rec.startswith('r')][0]

    sample_rec = final_recs[entry_key]
    rev_rec = final_recs['r{}'.format(entry_key)]

    print("Writing rec {} and decoy sequences".format(entry_key))
    print(sample_rec.seq)
    print(rev_rec.seq)

    errors = False
    if sample_rec.seq != rev_rec.seq[::-1]:
        print("ERROR: Sampled decoy sequence not reverse of original sequence")
        errors = True

    return errors

