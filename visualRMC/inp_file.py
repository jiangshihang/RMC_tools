#-*-coding:-utf-8-*-
import os
import sys
import re

class InputFile:
    
    def __init__(self, inputFileName):
        self.inputFile = open(inputFileName,'r')
        self.inputFileStr = self.inputFile.read()
        self.inputFile.close()
        
    def replace(self, regularExp, replaceStr):
        self.inputFileStr = re.sub(regularExp, replaceStr, self.inputFileStr)
        
    def toNewFile(self, newFileName):
        '''
        This function will help to write the changed file.
        If a file with the same name 'newFileName' already exists, the new file will replace it.
        '''
        newFile = open(newFileName, 'w')
        newFile.write(self.inputFileStr)
        newFile.close()
        
    def close(self):
        self.inputFile.close()
        
if __name__=='__main__':

    os.chdir(sys.path[0])
    
    inpFileName = 'inp_example'
    inpFile = InputFile(inpFileName)
    inpFile.replace('IDnum=\d+','IDnum=190')
    inpFile.toNewFile('inp_example')
