# -*- coding:utf-8 -*-
import os
import sys

import h5py as h5
import numpy as np


os.chdir(sys.path[0])


def get_array_from_h5(s_h5_name, s_array_name):
    """

    :param s_h5_name:
    :param s_array_name:
    :return:
    """
    f_h5 = h5.File(s_h5_name)
    s_dataset_name = '/'.join(['STATE_0001', s_array_name])
    np_property = f_h5[s_dataset_name]

    return np_property


def calc_assem_radial_ave(np_property, l_axial_location=[]):
    """

    :param np_property:
    :param l_axial_location:
    :return:
    """
    t_dimen = np_property.shape

    if l_axial_location == []:
        l_axial_location = range(0, t_dimen[2])
    np_assem_radial_ave = np.zeros([1, 1, t_dimen[2], t_dimen[3]])

    for i_assem in range(t_dimen[3]):
        for i_axial in l_axial_location:
            n_sum = np_property[:, :, i_axial, i_assem].sum()
            n_ave = n_sum / (t_dimen[0] * t_dimen[1])
            np_assem_radial_ave[0, 0, i_axial, i_assem] = n_ave

    return np_assem_radial_ave


def print_assem_radial_ave(np_assem_radial_ave, n_axial_location, l_core_map):
    """

    :param np_assem_radial_ave:
    :param n_axial_location:
    :param l_core_map:
    :return:
    """
    import math
    n_row = int(math.sqrt(len(l_core_map)))
    np_core_map = np.array(l_core_map).reshape(n_row, n_row)

    f_assem_radial_ave = open('assem_radial_ave', 'w')

    n_assem_count = 0
    for i_y in range(n_row):
        for i_x in range(n_row):
            f_assem_radial_ave.write('%-15.6f' % (np_assem_radial_ave[0, 0, n_axial_location, n_assem_count]
                                                  if np_core_map[i_x, i_y] != 0 else 0.0))
            if np_core_map[i_x, i_y] != 0:
                n_assem_count += 1

        f_assem_radial_ave.write('\n')

    f_assem_radial_ave.close()


def print_assem_radial_ave_sym(np_assem_radial_ave, n_axial_location, l_core_map):
    """

    :param np_assem_radial_ave:
    :param n_axial_location:
    :param l_core_map:
    :return:
    """
    import math
    n_row = int(math.sqrt(len(l_core_map)))
    np_core_map = np.array(l_core_map).reshape(n_row, n_row)
    np_assem_radial_ave_sym = np.zeros(len(l_core_map)).reshape(n_row, n_row)

    n_assem_count = 0
    for i_y in range(n_row):
        for i_x in range(n_row):
            if np_core_map[i_x, i_y] != 0:
                np_assem_radial_ave_sym[i_x, i_y] = np_assem_radial_ave[0, 0, n_axial_location, n_assem_count]
                n_assem_count += 1

    f_assem_radial_ave_sym = open('assem_radial_ave_sym', 'w')
    for i_y in range(n_row):
        for i_x in range(n_row):
            ave = (np_assem_radial_ave_sym[i_x, i_y] +
                   np_assem_radial_ave_sym[n_row - i_x - 1, i_y] +
                   np_assem_radial_ave_sym[i_x, n_row - i_y - 1] +
                   np_assem_radial_ave_sym[n_row - i_x - 1, n_row - i_y - 1]) / 4.0
            f_assem_radial_ave_sym.write('%-15.6f' % ave)
        f_assem_radial_ave_sym.write('\n')

    f_assem_radial_ave_sym.close()


def convert_np_to_tecplot(np_property, l_core_map):
    """

    :param:
    :return:
    """
    import math
    n_row = int(math.sqrt(len(l_core_map)))

    n_x, n_y, n_z, n_assem = np_property.shape
    np_core_map = np.array(l_core_map).reshape(n_row, n_row)
    np_tecplot = np.zeros(len(l_core_map) * n_x * n_y * n_z).reshape(n_row * n_x, n_row * n_y, n_z)

    i_assem = -1
    for i_x_assem in range(n_row):
        for i_y_assem in range(n_row):
            if np_core_map[i_x_assem, i_y_assem] != 0:
                i_assem += 1
                print 'processing data of assembly %d' % i_assem
            for i_z in range(n_z):
                for i_y_rod in range(n_y):
                    for i_x_rod in range(n_x):
                        np_tecplot[i_x_assem * n_x + i_x_rod, i_y_assem * n_y + i_y_rod, i_z] = \
                            (np_property[i_x_rod, i_y_rod, i_z, i_assem] * np_core_map[i_x_assem, i_y_assem])

    write_tecplot_file(np_tecplot)
    

def write_tecplot_file(np_tecplot):
    """

    :param np_tecplot:
    :return:
    """
    s_title = 'property from hdf5'  # todo using more flexible variable
    n_x, n_y, n_z = np_tecplot.shape

    with open('tecplot', 'w') as f_tecplot:
        f_tecplot.write('Title = \"%s\"\n' % s_title)
        f_tecplot.write('Variables = \"X\",\"Y\",\"Z\",\"%s\"\n' % s_title)
        f_tecplot.write('ZONE%sI = %d J = %d K = %d F=POINT\n' % (' ', n_x, n_y, n_z))
        # todo add "SOLUTION" to tecplot file

        for i_z in range(n_z):
            for i_y in range(n_y):
                for i_x in range(n_x):
                    f_tecplot.write('%-10d %-10d %-10d %-10.20f\n'
                                    % (i_x, i_y, i_z, np_tecplot[i_x, i_y, i_z]))


def get_array_from_dat(s_dat_name):
    """

    :param s_dat_name:
    :return:
    """

    np_ctf = np.zeros(get_dimen_from_dat(s_dat_name))

    # todo

    return np_ctf


def get_dimen_from_dat(s_dat_name):
    """

    :param s_dat_name:
    :return:
    """
    l_dimen = [1, 1, 1]

    # todo

    return l_dimen


if __name__ == '__main__':
    from optparse import OptionParser

    # command line parsing
    usage = """usage: %prog [options]"""
    parser = OptionParser(usage=usage)
    parser.add_option('-i', '--input', type='string', dest='input_name',
                      help='name of the data file.')
    parser.add_option('-p', '--property', type='string', dest='property_name',
                      help='name of the property.')
    parser.add_option('-t', '--type', type='string', dest='data_type',
                      help='type of the data file.\n'
                           'OPTIONS: hdf5; dat.')

    (options, args) = parser.parse_args()

    if options.input_name is not None:
        s_data_name = options.input_name
    else:
        s_data_name = 'pdeck.ctf_iter8.h5'

    if options.property_name is not None:
        s_property_name = options.property_name
    else:
        s_property_name = 'pin_powers'

    if options.data_type is not None:
        s_data_type = options.data_type.upper()
    else:
        s_data_type = 'HDF5'

    # define core map
    import re
    f_core_map = open('map', 'r')
    s_core_map = f_core_map.read()
    f_core_map.close()
    # s_core_map = '0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 ' \
    #              '0 0 1 1 1 1 1 1 1 1 1 1 1 0 0 ' \
    #              '0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 ' \
    #              '0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 ' \
    #              '1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ' \
    #              '1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ' \
    #              '1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ' \
    #              '1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ' \
    #              '1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ' \
    #              '1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ' \
    #              '1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ' \
    #              '0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 ' \
    #              '0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 ' \
    #              '0 0 1 1 1 1 1 1 1 1 1 1 1 0 0 ' \
    #              '0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 '
    l_core_map = re.findall('\d', s_core_map)
    l_core_map = [int(n_map) for n_map in l_core_map]

    # resolve h5 data
    if s_data_type == 'HDF5':

        np_property = get_array_from_h5(s_data_name, s_property_name)
        # np_assem_ave_property = calc_assem_radial_ave(np_property, [49])
        # print_assem_radial_ave_sym(np_assem_ave_property, 49, l_core_map)

        convert_np_to_tecplot(np_property, l_core_map)

    elif s_data_type == 'DAT':
        print "DAT data resolution not supported for now!"
        pass
    else:
        print "unrecognized data type. Only hdf5 and dat type supported."
        pass
