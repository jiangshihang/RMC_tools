# -*- coding:utf-8 -*-
import os
import sys


def run_kinetic():
    """

    :return:
    """
    from read_inp import read_inp
    from RMC import RMC

    from optparse import OptionParser

    # command line parsing
    usage = """usage: %prog [options]"""
    parser = OptionParser(usage=usage)
    parser.add_option('-n', '--mpi', type='int', dest='n_procs',
                      help="number of MPI parallel processes.")
    parser.add_option('-i', '--input', type='string', dest='input_name',
                      help="name of the input file.")
    parser.add_option('-p', '--platform', type='string', dest='platform',
                      help="name of the platform that the code is running on.\n"
                           "OPTIONS: linux, windows, tianhe, tansuo.")
    parser.add_option('-c', '--continue', type='string', dest='time',
                      help='timepoint to continue calculation.')

    (options, args) = parser.parse_args()

    if options.n_procs is not None:
        n_parallel = options.n_procs
    else:
        n_parallel = 1
    if options.input_name is not None:
        s_inp_name = options.input_name
    else:
        s_inp_name = 'inp'
    if options.platform is not None:
        s_platform = options.platform
    else:
        s_platform = 'LINUX'

    os.chdir(sys.path[0])
    if not os.path.exists('results'):
        os.mkdir('results')

    l_s_sub_inp_name = read_inp(s_inp_name)

    rmc = RMC()
    for i_sub_inp_name in range(len(l_s_sub_inp_name)):
        s_sub_inp_name = l_s_sub_inp_name[i_sub_inp_name]
        rmc.run(s_sub_inp_name, n_parallel, s_platform)
        rmc.archive(s_sub_inp_name, os.path.join(sys.path[0], 'results'))
        if i_sub_inp_name != len(l_s_sub_inp_name) - 1:
            os.rename(os.path.join(sys.path[0], s_sub_inp_name + '.source'),
                      os.path.join(sys.path[0], l_s_sub_inp_name[i_sub_inp_name + 1] + '.source'))


if __name__ == '__main__':
    run_kinetic()
