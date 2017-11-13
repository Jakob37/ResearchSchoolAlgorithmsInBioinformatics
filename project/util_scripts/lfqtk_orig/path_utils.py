import os


def get_basedir():
    basedir = os.path.dirname(os.path.realpath(__file__))
    return basedir
