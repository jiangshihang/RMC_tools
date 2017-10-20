# -*- coding:utf-8 -*-
import re


def read_inp(s_inp_name):
    """
    :param s_inp_name:
    :return:
    """
    s_inp = open(s_inp_name, 'r').read()

    s_inp = format_inp(s_inp)

    # open('pre_test_file', 'w').write(s_inp)

    # check_inp(s_inp)

    d_var_time = read_kinetic_para(s_inp)

    l_sub_inp_name = generate_inp(s_inp_name, s_inp, d_var_time)

    return l_sub_inp_name


def format_inp(s_inp):
    """
    function:
    0:add blanks around equals '='
    1:delete all comment;
    2:trans all lower-case letters to upper-case letters;
    3:delete all return character with a blank as the beginning of the next line;
    for input like this:
    UNIVERSE 11 move = 0 0 0  lat = 1  pitch = 1.26 1.26 1  scope = 17 17 1  fill=
     1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
     1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
    the output will be:
    UNIVERSE 11 MOVE = 0 0 0 LAT = 1 PITCH = 1.26 1.26 1 SCOPE = 17 17 1  FILL = 1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1 1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1
    :param s_inp: string of reading inp file
    :return: string after preconditioning
    """
    s_inp = s_inp.upper()

    l_inp = list(s_inp)

    # delete all '\r'
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '\r':
            del l_inp[index]
            n_del = 1
            n_len_inp -= 1
        index = index - n_del + 1
        n_del = 0

    # add blanks around equals '='
    index = 0
    n_insert = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '=':
            l_inp.insert(index + 1, ' ')
            l_inp.insert(index, ' ')
            n_insert = n_insert + 2
            n_len_inp = n_len_inp + 2
        index = index + n_insert + 1
        n_insert = 0

    # delete comments
    # delete a comment line
    index = 1
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '/' and l_inp[index - 1] == '\n':
            del l_inp[index - 1]
            n_len_inp -= 1
        index += 1
    # delete comment at end of a line
    n_slash_count = 0
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '/' and n_slash_count != 2:
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
            n_slash_count = n_slash_count + 1
        if n_slash_count == 2 and l_inp[index] != '\n':
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
        if n_slash_count == 2 and l_inp[index] == '\n':
            n_slash_count = 0
        index = index - n_del + 1
        n_del = 0

    # delete blanks
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 1:
        if l_inp[index] == ' ' and (l_inp[index + 1] == ' ' or l_inp[index + 1] == '\n'):
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
        index = index - n_del + 1
        n_del = 0

    # delete redundant returns
    # delete returns with a blank following
    index = 0
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp - 1:
        if l_inp[index] == '\n' and l_inp[index + 1] == ' ':
            del l_inp[index]
            n_len_inp = n_len_inp - 1
            n_del = 1
        index = index - n_del + 1
        n_del = 0
    # delete more than three consecutive returns
    index = 2
    n_del = 0
    n_len_inp = len(l_inp)
    while index < n_len_inp:
        if l_inp[index] == '\n' and l_inp[index - 1] == '\n' and l_inp[index - 2] == '\n':
            del l_inp[index]
            n_del += 1
            n_len_inp -= 1
        index = index - n_del + 1
        n_del = 0

    # delete returns at file beginning and ending
    # delete returns at file beginning
    while l_inp[0] == '\n':
        del l_inp[0]
    # delete all returns at file ending
    index = len(l_inp) - 1
    while l_inp[index] == '\n':
        del l_inp[index]
        index = index - 1
    # add a return at file ending
    l_inp.append('\n')

    return ''.join(l_inp)


def read_kinetic_para(s_inp):
    """
    function:


    :param s_inp:
    :return:
    {'INDEX_KINETIC':4000,
     'FIT':{'FITSTEP':['5', '10', '15']
                'SAMPLESTEP':[['0', '1', '2', '4'],
                              ['5', '6', '7', '8'],
                              ['11','12','14','15']]
                'SUBSTEP':['100', '100', '100']
                }
     'TIMESTEP':[time0, time1, time2, ..., time15],
     'PARAMETER':{'LOCALWORD':['SURF 18 PZ', 'SURF 19 PZ']
                  'VALUE':[[[value for time0], [value for time1], [value for time2], ..., [value for time15]],
                           [[value for time0], [value for time1], [value for time2], ..., [value for time15]]
                          ]
                 }
     }
    """
    d_kinetic_para = {}

    l_key = ['KINETIC',
             'FIT', 'FITSTEP', 'SAMPLESTEP', 'SUBSTEP', 'MODE',
             'TIMESTEP', 'TIME',
             'PARAMETER', 'LOCALWORD', 'VALUE']

    i_kinetic = s_inp.index('KINETIC')
    d_kinetic_para['INDEX_KINETIC'] = i_kinetic

    s_kinetic_block = s_inp[i_kinetic:]

    i_quadfit = s_kinetic_block.find('FIT')
    i_timestep = s_kinetic_block.index('TIMESTEP')
    i_parameter = s_kinetic_block.index('PARAMETER')
    if i_quadfit != -1:
        s_quadfit_block = s_kinetic_block[i_quadfit + 4: i_timestep]
    s_timestep_block = s_kinetic_block[i_timestep + 9: i_parameter]
    s_parameter_block = s_kinetic_block[i_parameter + 10:]

    # read fit
    if i_quadfit != -1:
        d_kinetic_para['FIT'] = {}
        d_kinetic_para['FIT']['FITSTEP'] = []
        d_kinetic_para['FIT']['SAMPLESTEP'] = []
        d_kinetic_para['FIT']['SUBSTEP'] = []
        d_kinetic_para['FIT']['MODE'] = []

        i_cur_keyword = 0
        while i_cur_keyword != -1:
            l_fitstep, i_cur_keyword = get_key_value(s_quadfit_block, i_cur_keyword, 'FITSTEP', l_key)
            l_samplestep, i_cur_keyword = get_key_value(s_quadfit_block, i_cur_keyword, 'SAMPLESTEP', l_key)
            l_substep, i_cur_keyword = get_key_value(s_quadfit_block, i_cur_keyword, 'SUBSTEP', l_key)
            l_mode, i_cur_keyword = get_key_value(s_quadfit_block, i_cur_keyword, 'MODE', l_key)
            d_kinetic_para['FIT']['FITSTEP'].append(l_fitstep[0])
            d_kinetic_para['FIT']['SAMPLESTEP'].append(l_samplestep)
            d_kinetic_para['FIT']['SUBSTEP'].append(l_substep[0])
            d_kinetic_para['FIT']['MODE'].append(l_mode[0])

    # read time
    d_kinetic_para['TIMESTEP'] = []
    i_cur_keyword = 0
    while i_cur_keyword != -1:
        l_time, i_cur_keyword = get_key_value(s_timestep_block, i_cur_keyword, 'TIME', l_key)
        for s_time in l_time:
            d_kinetic_para['TIMESTEP'].append(s_time)

    # read parameter
    d_kinetic_para['PARAMETER'] = {}
    d_kinetic_para['PARAMETER']['LOCALWORD'] = []
    d_kinetic_para['PARAMETER']['VALUE'] = []
    i_cur_keyword = 0
    while i_cur_keyword != -1:
        l_localword, i_cur_keyword = get_key_value(s_parameter_block, i_cur_keyword, 'LOCALWORD', l_key)
        l_value, i_cur_keyword = get_key_value(s_parameter_block, i_cur_keyword, 'VALUE', l_key)
        d_kinetic_para['PARAMETER']['LOCALWORD'].append(' '.join(l_localword))
        l_value_grouped = []
        n_timestep = len(d_kinetic_para['TIMESTEP'])
        n_value = len(l_value)
        for i in range(len(d_kinetic_para['TIMESTEP'])):
            l_value_grouped.append(l_value[i * n_value / n_timestep:(i + 1) * n_value / n_timestep])
        d_kinetic_para['PARAMETER']['VALUE'].append(l_value_grouped)

    return d_kinetic_para


def get_key_value(s_block, i_cur, s_key, s_key_list):
    """
    function:
    1.get the value of 's_key'
    2.move the index 'i_cur' to the beginning of the next key
    :param s_block:
    :param i_cur:
    :param s_key:
    :param s_key_list:
    :return:
    """
    l_key_value = []

    s_key_block = s_block[i_cur:]
    i_cur = i_cur + s_key_block.index(s_key)

    b_record_key_value = False
    i_cur = get_next_word_index(i_cur, s_block)
    s_next_word = get_next_word(i_cur, s_block)

    while s_next_word not in s_key_list and s_next_word != 'NULL':
        if s_next_word == '=':
            b_record_key_value = True
        elif b_record_key_value:
            l_key_value.append(s_next_word)
        i_cur = get_next_word_index(i_cur, s_block)
        s_next_word = get_next_word(i_cur, s_block)

    return l_key_value, i_cur


def get_next_separator_index(i_cur_word, s_block):
    """

    :param i_cur_word:
    :param s_block:
    :return:
    """
    i_next_separator = i_cur_word
    # add a separator to the end if there is no separator at end
    b_separator_end = True
    if s_block[-1] != ' ' and s_block != '\n':
        b_separator_end = False
        s_block = s_block + '\n'
    # move the index until the index points to a separator
    while s_block[i_next_separator] != ' ' and s_block[i_next_separator] != '\n' and s_block[i_next_separator] != '\t':
        i_next_separator = i_next_separator + 1
    # if there is no separator behind the current index, return -1
    if i_next_separator == len(s_block) - 1 and not b_separator_end:
        i_next_separator = -1
    return i_next_separator


def get_next_word_index(i_cur_word, s_block):
    """

    :param i_cur_word:
    :param s_block:
    :return:
    """
    i_next_word = get_next_separator_index(i_cur_word, s_block)
    if i_next_word != -1:
        i_next_word = i_next_word + 1
    if i_next_word == len(s_block):
        i_next_word = -1
    return i_next_word


def get_next_word(i_cur_word, s_block):
    """

    :param i_cur_word:
    :param s_block:
    :return:
    """
    i_next_separator = get_next_separator_index(i_cur_word, s_block)
    if i_next_separator == -1:
        s_next_word = 'NULL'
    else:
        s_next_word = s_block[i_cur_word: i_next_separator]

    return s_next_word


def generate_inp(s_inp_name, s_inp, d_var_time):
    """

    :param s_inp_name:
    :param s_inp:
    :param d_var_time:
    :return:
    """
    l_sub_inp_name = []

    l_n_time = []
    for s_time in d_var_time['TIMESTEP']:
        l_n_time.append(float(s_time))
    l_n_time.append(l_n_time[-1] + 1.0)

    i_kinetic = d_var_time['INDEX_KINETIC']
    s_sub_inp_origin = s_inp[:i_kinetic]

    for i_time in range(len(l_n_time[:-1])):
        n_time = l_n_time[i_time]
        n_delta_time = l_n_time[i_time + 1] - l_n_time[i_time]

        s_sub_inp = s_sub_inp_origin

        # delete INITSRC POINT key_and_value for dynamic state
        if n_time != 0.0:
            # get all chars in line containing 'INITSRC POINT'
            i_init_src_start = s_sub_inp.index('INITSRC POINT')
            i_init_src_end = i_init_src_start
            while s_sub_inp[i_init_src_end] != '\n':
                i_init_src_end = i_init_src_end + 1
            s_target = s_sub_inp[i_init_src_start: i_init_src_end + 1]
            s_replace = ''
            s_sub_inp = modify_inp(s_sub_inp, s_target, s_replace)

        # change QUASISTATIC block name
        s_target = 'QUASISTATIC'
        if n_time == 0.0:
            s_replace = 'QUASISTATIC_S'
        else:
            s_replace = 'QUASISTATIC_D'
        s_sub_inp = modify_inp(s_sub_inp, s_target, s_replace)

        # change timestep
        s_target = 'TIMESTEP'
        s_replace = 'TIMESTEP DELTAT = %s' % n_delta_time
        s_sub_inp = modify_inp(s_sub_inp, s_target, s_replace)

        # change quadfit
        if 'FIT' in d_var_time:
            s_target = 'FIT'
            s_replace = 'FIT'

            # add currentstep
            if n_time != 0:
                s_replace += ' CURRENTSTEP = %s' % i_time

            # add samplestep and substep
            s_fitstep = '%s' % i_time
            if s_fitstep in d_var_time['FIT']['FITSTEP']:
                i_fitstep = d_var_time['FIT']['FITSTEP'].index(s_fitstep)

                s_replace += ' SAMPLESTEP = ' + ' '.join(d_var_time['FIT']['SAMPLESTEP'][i_fitstep])
                s_replace += ' SUBSTEP = ' + d_var_time['FIT']['SUBSTEP'][i_fitstep]
                s_replace += ' MODE = ' + d_var_time['FIT']['MODE'][i_fitstep]

            s_sub_inp = modify_inp(s_sub_inp, s_target, s_replace)

        # change kinetic parameters
        for s_parameter in d_var_time['PARAMETER']['LOCALWORD']:
            i_parameter = d_var_time['PARAMETER']['LOCALWORD'].index(s_parameter)

            s_target = s_parameter
            s_replace = s_parameter

            s_replace += ' ' + ' '.join(d_var_time['PARAMETER']['VALUE'][i_parameter][i_time])

            i_cur_word = s_sub_inp.index(s_target) + len(s_target) + 1
            for s_value in d_var_time['PARAMETER']['VALUE'][i_parameter][i_time]:
                s_next_word = get_next_word(i_cur_word, s_sub_inp)
                i_cur_word = get_next_word_index(i_cur_word, s_sub_inp)
                s_target += ' ' + s_next_word

            s_sub_inp = modify_inp(s_sub_inp, s_target, s_replace)

        s_sub_inp_name = s_inp_name + '.%s' % n_time
        l_sub_inp_name.append(s_sub_inp_name)

        f_sub_inp = open(s_sub_inp_name, 'w')
        f_sub_inp.write(s_sub_inp)
        f_sub_inp.close()

    return l_sub_inp_name


def modify_inp(s_inp, s_target, s_replace):
    """

    :param s_inp:
    :param s_target:
    :param s_replace:
    :return:
    """
    l_inp = list(s_inp)
    i_target = s_inp.index(s_target)
    for n_del in range(len(s_target)):
        del l_inp[i_target]
    l_inp.insert(i_target, s_replace)
    return ''.join(l_inp)


def check_inp(s_inp):
    """
    function: check the inp file
    1.make sure the block "KINETIC" occurs only once
    2.make sure the keyword "TIME" and "PARAMETER" exists
      make sure the keyword "TIME" occurs only once
      make sure the keywords are in right order: "QUADFIT" first (if exists), "TIME" second and "PARAMETER" third
    3.make sure the block "QUASISTATIC" exists and occurs only once
    4.make sure that if "QUADFIT" exists in "KINETIC" block,
      then "QUADFIT" exists in "QUASISTATIC", too.
    :param s_inp:
    :return:
    """


def check_kinetic_para(d_var_kinetic):
    """
    functions:
    1.make sure TIME exists and 0.0 exists
    2.make sure TIME and every PARAMETER have the same dimension
    3.make sure QUADFIT have the corresponding dimension if this keyword exists
    4.make sure every PARAMETER exists in the inp file
    :param d_var_kinetic:
    :return:
    """


if __name__ == '__main__':
    read_inp('test_inp')
