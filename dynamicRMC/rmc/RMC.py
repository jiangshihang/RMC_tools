# -*- coding:utf-8 -*-
import os
import sys
import shutil
import time


class RMC:
    """

    """
    def __init__(self, s_rmc_name='RMC', s_inp_name='inp'):
        """

        :param s_name:
        """
        self.s_rmc_name = s_rmc_name
        self.s_inp_name = s_inp_name

    def run(self, n_parallel, s_platform):
        """

        :param s_inp_name:
        :param n_parallel:
        :param s_platform:
        :return:
        """
        s_platform = s_platform.upper()
        if s_platform == 'WINDOWS':
            self._run_windows(n_parallel)
        elif s_platform == 'LINUX':
            self._run_linux(n_parallel)
        elif s_platform == 'TIANHE':
            self._run_tianhe(n_parallel)
        elif s_platform == 'TANSUO':
            self._run_tansuo(n_parallel)
        elif s_platform == 'SHENWEI':
            self._run_shenwei(n_parallel)
        else:
            print 'ERROR! unrecognized platform: ' + s_platform
            raise IOError

    def _run_windows(self, n_parallel):
        """

        :param s_inp_name:
        :param n_parallel:
        :return:
        """
        os.system('mpiexec -n %s %s.exe %s' % (n_parallel, self.s_rmc_name, self.s_inp_name))
    
    def _run_linux(self, n_parallel):
        """

        :param s_inp_name:
        :param n_parallel:
        :return:
        """
        os.system('mpiexec -n %s ./%s %s' % (n_parallel, self.s_rmc_name, self.s_inp_name))
    
    def _run_simulator(self, s_simulator_name):
        """

        :param s_simulator_name:
        :return:
        """
        os.system('python %s' % s_simulator_name)
        
    def _run_tianhe(self, n_parallel=23):
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
            os.system('yhrun -n %s ./%s %s' % (n_parallel, self.s_rmc_name, self.s_inp_name))
            write_log('Job submitted!')
            # check if the submission succeeds
            if os.path.exists(self.s_inp_name + '.out'):
                b_running = True
                write_log('Job submission succeeded!')
            else:
                write_log('Job submission failed!')
                time.sleep(60)
                write_log('Retry submission...')
        
    def _run_tansuo(self, n_parallel=24):
        """
        Run RMC on Tansuo100.
        """
        import subprocess

        # job submission
        s_tansuo_job_format =  'bsub -q hpc_linux -a intelmpi -n {0} -o out.{1}.\%J -e err.{1}.\%J mpirun.lsf ./{2} {1}'
        s_tansuo_job =s_tansuo_job_format.format(n_parallel, self.s_inp_name, self.s_rmc_name)
        b_sub_success = False
        while not b_sub_success:
            # submit job
            p_tansuo = subprocess.Popen(s_tansuo_job, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            s_output = ''
            while p_tansuo.poll() is None:
                s_output += p_tansuo.stdout.read()

            write_log('Job submitted!')
            write_log(s_output)

            if not os.path.exists(self.s_inp_name + 'out'):
                b_sub_success = True
                write_log('Job submission succeeded!')
            else:
                write_log('Job submission failed!')
                time.sleep(30)
                write_log('Retry submission...')

        # wait for calculation finish
        self._wait_job_end()
        
    def _run_shenwei(self, n_parallel=24):
        """
        Run RMC on SHENWEI.
        """
        import subprocess

        # job submission
        s_tansuo_job_format =  'bsub -q q_x86_share -n {0} -o out.{1}.\%J mpirun ./{2} {1}'
        s_tansuo_job =s_tansuo_job_format.format(n_parallel, self.s_inp_name, self.s_rmc_name)
        b_sub_success = False
        while not b_sub_success:
            # submit job
            p_tansuo = subprocess.Popen(s_tansuo_job, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            s_output = ''
            while p_tansuo.poll() is None:
                s_output += p_tansuo.stdout.read()

            write_log('Job submitted!')
            write_log(s_output)

            if not os.path.exists(self.s_inp_name + 'out'):
                b_sub_success = True
                write_log('Job submission succeeded!')
            else:
                write_log('Job submission failed!')
                time.sleep(30)
                write_log('Retry submission...')

    def _wait_job_end(self):
        """
        Wait until rmc ends by reading rmc output files.
        """
        # if rmc.out file does not exist, wait
        s_rmc_out_name = self.s_inp_name + '.out'
        while not os.path.exists(s_rmc_out_name):
            time.sleep(1)

        # if rmc.out file is toooo small, wait
        while os.path.getsize(s_rmc_out_name) < 3000:
            time.sleep(1)

        # if rmc.out file is still changing, wait
        n_out_file_size = 0
        changing = True
        while changing:
            changing = os.path.getsize(s_rmc_out_name) != n_out_file_size
            n_out_file_size = os.path.getsize(s_rmc_out_name)
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
    
    RMC = RMC('inp')
    RMC.run(24, 'linux')
    RMC.archive('inp')
