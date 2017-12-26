#-*- coding: utf-8 -*-
import os
import sys
import re
import numpy as np
from optparse import OptionParser

class meshTally:
    '''
    
    '''
    def __init__(self, tallyFileName, inpFileName):
        '''
        scope: a dictionary with the following structure:
        {'idnum' : the total id counts in the meshtally file,
         'id1' : [x counts of tally id 1, y counts of tally id 1, z counts of tally id 1]
         'id2' : [x counts of tally id 2, y counts of tally id 2, z counts of tally id 2]
         ...
         'idn' : [x counts of tally id n, y counts of tally id n, z counts of tally id n]
        }
        
        data: a dictionary with the following structure:
        {'id1' : array1(structure:[x][y][z])
         'id2' : array2(structure:[x][y][z])
         ...
         'idn' : arrayn(structure:[x][y][z])
        }
        '''
        self.tallyFileName = tallyFileName
        self.inpFileName = inpFileName

        self.id = 1
        self.scope = self.__getScope(self.inpFileName)
        self.boundary = self.__getBoundary(self.inpFileName)
        
        self.data = {}
        for id in self.scope:
            if id != 'idnum':
                x_scope = self.scope[id][0]
                y_scope = self.scope[id][1]
                z_scope = self.scope[id][2]
                self.data[id] = np.empty(x_scope*y_scope*z_scope).reshape(x_scope, y_scope, z_scope)
        
    def __getScope(self, inpFileName):
        '''
        
        '''
        inpFile = open(inpFileName)
        scopeTupleList = re.findall('MeshTally\s*(\d+).*Scope\s*=\s*(\d+)\s*(\d+)\s*(\d+)\s*',inpFile.read())
        inpFile.close()
        
        scope = {'idnum' : len(scopeTupleList)}
        
        for i in range(len(scopeTupleList)):
            scope['id'+scopeTupleList[i][0]] = [int(scopeTupleList[i][1]),int(scopeTupleList[i][2]),int(scopeTupleList[i][3])]
            
        return scope
        
    def __getBoundary(self, inpFileName):
        '''

        '''
        inpFile = open(inpFileName)
        boundTupleList = re.findall('MeshTally\s*(\d+).*Scope\s*=\s*\d+\s*\d+\s*\d+\s*Bound\s*=\s*([\.\d]+)\s+([\.\d]+)\s+([\.\d]+)\s+([\.\d]+)\s+([\.\d]+)\s+([\.\d]+)',inpFile.read())
        inpFile.close()
        
        bound = {'idnum' : len(boundTupleList)}
        
        for i in range(len(boundTupleList)):
            bound['id'+boundTupleList[i][0]] = [ [0.1*float(boundTupleList[i][1]),0.1*float(boundTupleList[i][2])],\
                                                 [0.1*float(boundTupleList[i][3]),0.1*float(boundTupleList[i][4])],\
                                                 [0.1*float(boundTupleList[i][5]),0.1*float(boundTupleList[i][6])] ]
            
        return bound

    def setId(self, idInput):
        '''
        
        '''
        self.id = idInput
        
    def getScope(self):
        '''
        
        '''
        return self.scope['id%s'%self.id]

    def getBoundary(self):
        '''

        '''
        return self.boundary['id%s'%self.id]
        
    def getData(self):
        '''
        
        '''
        tallyFile = open(self.tallyFileName)
        
        idKey = 'id%s'%self.id
        findId = False
        lineAfterId = 0
        
        for line in tallyFile:
            idLineRe = 'ID = %s'%self.id
            findId = findId or re.findall(idLineRe, line) != []
            if findId == True:
                if lineAfterId == 0 or lineAfterId == 1:
                    lineAfterId += 1
                elif lineAfterId > 1 and lineAfterId <= self.scope[idKey][0]*self.scope[idKey][1]*self.scope[idKey][2]+1:
                    coordAndValue = re.findall('(\d+)\s+(\d+)\s+(\d+)\s+([.\d]+[Ee][+-]\d+)',line)
                    xcoord = int(coordAndValue[0][0])
                    ycoord = int(coordAndValue[0][1])
                    zcoord = int(coordAndValue[0][2])
                    self.data[idKey][xcoord-1, ycoord-1, zcoord-1] = float(coordAndValue[0][3])
                    lineAfterId += 1
                else:
                    break
        
        tallyFile.close()
        return self.data[idKey]
        
if __name__=='__main__':
    
    test_dir = os.path.join('tests', 'mesh_tally')
    os.chdir(test_dir)

    usage = """usage: %prog [options]"""
    parser = OptionParser(usage=usage)
    parser.add_option('-t', '--tally', dest='tallyFileName', default='inp.tally',
                      help='Name of the tally file, Default: inp.tally')
    parser.add_option('-i', '--input', dest='inpFileName', default='inp',
                      help='Name of the input file, Default: inp')

    (options, args) = parser.parse_args()

    tallyFileName = options.tallyFileName
    inpFileName = options.inpFileName

    testMeshTally = meshTally(tallyFileName, inpFileName)
    testMeshTally.setId(35)
    print testMeshTally.getScope()

    testMeshTally.setId(1)
    meshData = testMeshTally.getData()
    print meshData.shape
    print meshData