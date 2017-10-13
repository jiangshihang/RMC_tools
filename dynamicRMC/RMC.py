# -*- coding:utf-8 -*-
import os
import sys
import shutil
import time


class RMC:
    """

    """
    def __init__(self, s_name='RMC'):
        """

        :param s_name:
        """
        self.s_rmc_name = s_name

    def run(self, s_inp_name, n_parallel, s_platform):
        """

        :param s_inp_name:
        :param n_parallel:
        :param s_platform:
        :return:
        """
        s_platform = s_platform.upper()
        if s_platform == 'WINDOWS':
            self._run_windows(s_inp_name, n_parallel)
        elif s_platform == 'LINUX':
            self._run_linux(s_inp_name, n_parallel)
        elif s_platform == 'TIANHE':
            self._run_tianhe(s_inp_name, n_parallel)
        elif s_platform == 'TANSUO':
            self._run_tansuo(s_inp_name)
        elif s_platform == 'SHENWEI':
            self._run_tansuo(s_inp_name)
        else:
            print 'ERROR! unrecognized platform ' + s_platform
            raise IOError

    def _run_windows(self, s_inp_name, n_parallel):
        """

        :param s_inp_name:
        :param n_parallel:
        :return:
        """
        os.system('mpiexec -n %s %s.exe %s' % (n_parallel, self.s_rmc_name, s_inp_name))
    
    def _run_linux(self, s_inp_name, n_parallel):
        """

        :param s_inp_name:
        :param n_parallel:
        :return:
        """
        os.system('mpiexec -n %s ./%s %s' % (n_parallel, self.s_rmc_name, s_inp_name))
    
    def _run_simulator(self, s_simulator_name):
        """

        :param s_simulator_name:
        :return:
        """
        os.system('python %s' % s_simulator_name)
        
    def _run_tianhe(self, s_inp_name, n_parallel=23):
        """
        function: Run RMC on Tianhe2.
        caution: Because the submission error often occurs on Tianhe2,
                 a detective method is used in this function, which is simply checking if the inp.out file exists.
        :param s_inp_name:
        :param n_parallel:
        :return:
        """
        b_running = False
        while not b_running:
            # submit job
            os.system('yhrun -n %s ./%s %s' % (n_parallel, self.s_rmc_name, s_inp_name))
            write_log('Job submitted!')
            # check if the submission succeeds
            if os.path.exists(s_inp_name + '.out'):
                b_running = True
                write_log('Job submission succeeded!')
            else:
                write_log('Job submission failed!')
                time.sleep(60)
                write_log('Retry submission...')
        
    def _run_tansuo(self, s_inp_name, n_parallel=24):
        """
        AIM: Run RMC on Tansuo100.
        COMMENT: This function will not use the parallel_core_number input.
        """
        # job submission
        # todo: create job scripts using s_inp_name and n_parallel and then bsub < job
        os.system('bsub < %s' % s_inp_name)
        # wait for calculation finish
        while not os.path.exists(s_inp_name + '.out'):
            time.sleep(30)
        while os.path.getsize(s_inp_name + '.out') < 3000:
            time.sleep(1)
        old_file_size = 0
        while os.path.getsize(s_inp_name + '.out') != old_file_size:
            old_file_size = os.path.getsize(s_inp_name + '.out')
            time.sleep(1)

    def archive(self, s_inp_name, s_to_dir='default', suffix=''):
        """

        :param s_inp_name:
        :param s_to_dir:
        :param suffix:
        :return:
        """
        if s_to_dir == 'default':
            s_to_dir = sys.path[0]

        if os.path.exists(os.path.join(sys.path[0], s_inp_name)):
            os.rename(os.path.join(sys.path[0], s_inp_name),
                      os.path.join(s_to_dir, s_inp_name + suffix))
        if os.path.exists(os.path.join(sys.path[0], s_inp_name + '.tally')):
            os.rename(os.path.join(sys.path[0], s_inp_name + '.tally'),
                      os.path.join(s_to_dir, s_inp_name + suffix + '.tally'))
        if os.path.exists(os.path.join(sys.path[0], s_inp_name + '.Tally')):
            os.rename(os.path.join(sys.path[0], s_inp_name + '.Tally'),
                      os.path.join(s_to_dir, s_inp_name + suffix + '.Tally'))
        if os.path.exists(os.path.join(sys.path[0], s_inp_name + '.material')):
            os.rename(os.path.join(sys.path[0], s_inp_name + '.material'),
                      os.path.join(s_to_dir, s_inp_name + suffix + '.material'))
        if os.path.exists(os.path.join(sys.path[0], s_inp_name + '.out')):
            os.rename(os.path.join(sys.path[0], s_inp_name + '.out'),
                      os.path.join(s_to_dir, s_inp_name + suffix + '.out'))
        if os.path.exists(os.path.join(sys.path[0], s_inp_name + '.innerproduct')):
            os.rename(os.path.join(sys.path[0], s_inp_name + '.innerproduct'),
                      os.path.join(s_to_dir, s_inp_name + suffix + '.innerproduct'))

        if os.path.exists(os.path.join(sys.path[0], s_inp_name + '.source')):
            shutil.copyfile(os.path.join(sys.path[0], s_inp_name + '.source'),
                            os.path.join(s_to_dir, s_inp_name + suffix + '.source'))


def write_log(content):
    """

    :param content:
    :return:
    """
    localtime = time.asctime(time.localtime(time.time()))
    f_log_file = open('RMC.log', 'a')
    f_log_file.write('Time: %s  ' % localtime+content+'\n')
    f_log_file.close()


if __name__ == '__main__':
    
    RMC = RMC()
    RMC.run('inp', 4, 'linux')
    RMC.archive('inp')
