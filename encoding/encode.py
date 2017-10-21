# -*- coding:utf-8 -*-
import os
import sys
import glob
import shutil

os.chdir(sys.path[0])

# todo output warning message to remind users to install enca on their machine.

l_file_name = glob.glob('*.*')

for s_file_name in l_file_name:
    # backup
    shutil.copyfile(s_file_name, ''.join([s_file_name, '.backup']))
    # transcoding
    os.system(''.join(['enca -L zh_CN -x UTF-8 ', s_file_name]))

