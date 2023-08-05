#!/usr/bin/env python3
# author          : Alina Kutlushina
# date            : 01.05.2018
# license         : BSD-3
#==============================================================================
import os
import sys
import time

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from multiprocessing import Process

from .scripts import gen_stereo_rdkit, gen_conf_rdkit, split
from .scripts import create_db


def create_parser():
    parser = ArgumentParser(description='', formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', metavar='input.smi', type=str, required=True,
                        help='input smi file or multiple files')
    parser.add_argument('-f', '--rdkit_factory', metavar='features.fdef', default=None,
                        help='text file with definition of pharmacophore features in RDKit format. If file name is not '
                             'specified the default file from the script dir will be used. This option has '
                             'a priority over smarts_features.')
    parser.add_argument('-n', '--nconf', metavar='conf_number', default=100,
                        help='number of generated conformers.')
    parser.add_argument('-e', '--energy_cutoff', metavar='100', default=100,
                        help='conformers with energy difference from the lowest one greater than the specified '
                             'value will be discarded.')
    parser.add_argument('-r', '--rms', metavar='rms_threshold', default=0.5,
                        help='only conformers with RMS higher then threshold will be kept.')
    parser.add_argument('-c', '--ncpu', metavar='cpu_number', default=1,
                        help='number of cpus to use for processing of actives and inactives separately. ')
    return parser


def common(filenames, nconf, energy, rms, rdkit_factory, ncpu, set_name):
    start = time.time()

    input_fname = filenames[0]

    gen_stereo_rdkit.main_params(in_fname=input_fname,
                                 out_fname=filenames[2],
                                 tetrahedral=True,
                                 double_bond=True,
                                 max_undef=-1,
                                 id_field_name=None,
                                 ncpu=ncpu,
                                 verbose=True)

    gen_conf_rdkit.main_params(in_fname=filenames[2],
                               out_fname=filenames[3],
                               id_field_name=None,
                               nconf=nconf,
                               energy=energy,
                               rms=rms,
                               ncpu=ncpu,
                               seed=-1,
                               verbose=True)

    create_db.main_params(dbout_fname=filenames[4],
                          smarts_features_fname=None, 
                          rdkit_factory=rdkit_factory,
                          conformers_fname=filenames[3],
                          bin_step=1,
                          rewrite_db=True,
                          id_field_name=None,
                          stereo_id=True,
                          verbose=True,
                          ncpu=ncpu)

    sys.stderr.write('prepare {} dataset ({}s)'.format(set_name, time.time() - start))


def main(in_fname, rdkit_factory, nconf, energy, rms, ncpu):
    """
    launches the entire cycle of data preprocessing: generation of stereoisomers, conformers and a database
    :param in_fname: input .smi file containing information about SMILES, compounds id and its activity status
    :param split_dataset: if True will splited input dasets into active and inactive sets else will not
    :param rdkit_factory: text file with definition of pharmacophore features in RDKit format.
    :param nconf: max number of generated conformers
    :param energy: conformers with energy difference from the lowest one greater than the specified value will be discarded.
    :param rms: only conformers with RMS higher then threshold will be kept.
    :param ncpu: number of cpus to use for processing of actives and inactives separately.
    :return:
    """

    comm_path = os.path.join(os.path.dirname(os.path.abspath(in_fname)), 'compounds')
    if not os.path.exists(comm_path):
        os.mkdir(comm_path)

    mol_act = os.path.join(comm_path, 'active.smi')
    mol_inact = os.path.join(comm_path, 'inactive.smi')
    split.main(in_fname, mol_act, mol_inact)
    in_fname = [mol_act, mol_inact]

    procs = []
    for index, fname in enumerate(in_fname):
        nickname = os.path.basename(fname).split('.')[0]
        list_ts = [fname,
                   os.path.join(comm_path, '{}_taut.sdf'.format(nickname)),
                   os.path.join(comm_path, '{}_stereo.smi'.format(nickname)),
                   os.path.join(comm_path, '{}_conf.sdf'.format(nickname)),
                   os.path.join(comm_path, '{}.db'.format(nickname))]
        proc = Process(target=common, args=(list_ts, nconf, energy, rms, rdkit_factory,
                                            ncpu, nickname))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


def entry_point():
    parser = create_parser()
    args = vars(parser.parse_args())
    for o, v in args.items():
        if o == "input": in_fname = v
        if o == "rdkit_factory": rdkit_factory = v
        if o == "nconf": nconf = int(v)
        if o == "energy_cutoff": energy = float(v)
        if o == "rms": rms = float(v) if v is not None else None
        if o == "ncpu": ncpu = int(v)

    main(in_fname=in_fname,
         rdkit_factory=rdkit_factory,
         nconf=nconf,
         energy=energy,
         rms=rms,
         ncpu=ncpu)


if __name__ == '__main__':
    entry_point()
