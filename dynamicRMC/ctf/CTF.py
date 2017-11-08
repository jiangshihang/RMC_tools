# -*- coding:utf-8 -*-

import os


class CTF:
    """

    """
    def __init__(self, cobratf='./cobratf', inp='deck.inp', platform='LINUX'):
        self.cobratf = cobratf
        self.inp = inp
        self.platform = platform

    def run(self, parallel_core_number=4):
        if self.platform == 'LINUX':
            self.__run_linux(parallel_core_number)

    def __run_linux(self, parallel_core_number=1):
        if parallel_core_number == 1:
            os.system('%s %s' % (self.cobratf, self.inp))
        else:
            os.system('mpiexec -n %s %s %s' % (parallel_core_number, self.cobratf, self.inp))

    def tidy(self):  # todo
        return


class CTFPreproc:
    """


    """
    def __init__(self, cobratf_preproc='./cobratf_preproc', platform='LINUX'):
        self.cobratf_preproc = cobratf_preproc
        self.platform = platform

    def run(self):
        if self.platform == 'LINUX':
            self.__run_linux()

    def __run_linux(self):
        os.system('%s' % self.cobratf_preproc)

    def tidy(self):  # todo
        return
