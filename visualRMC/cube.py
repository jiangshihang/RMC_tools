# -*- coding=utf-8 -*-
import os
import sys

class cubeWriter:
    '''

    '''
    def __init__(self, scope, data_set, property_name, boundary):
        #
        [self.xcount, self.ycount, self.zcount] = scope
        self.data_set = data_set
        self.property_name = property_name

        [self.xbound, self.ybound, self.zbound] = boundary

        self.xstep = (self.xbound[1]-self.xbound[0])/self.xcount
        self.ystep = (self.ybound[1]-self.ybound[0])/self.ycount
        self.zstep = (self.zbound[1]-self.zbound[0])/self.zcount

        self.xorigin = min(self.xbound[0], self.xbound[1]) + self.xstep/2
        self.yorigin = min(self.ybound[0], self.ybound[1]) + self.ystep/2
        self.zorigin = min(self.zbound[0], self.zbound[1]) + self.zstep/2

    def write(self, file_name):
        #
        cube_file = open(file_name, 'w')
        cube_file.write('# vtk DataFile Version 2.0\n')
        cube_file.write('CUBE\n')
        cube_file.write('ASCII\n')
        cube_file.write('DATASET STRUCTURED_POINTS\n')
        cube_file.close()

        self.__write_dimension(file_name)
        self.__write_scalars(file_name)

    def __write_dimension(self, file_name):
        #
        cube_file = open(file_name, 'a')
        cube_file.write('DIMENSIONS %s %s %s\n'%(self.xcount, self.ycount, self.zcount))
        cube_file.write('SPACING %s %s %s\n'%(self.xstep, self.ystep, self.zstep))
        cube_file.write('ORIGIN %s %s %s\n'%(self.xorigin, self.yorigin, self.zorigin))
        cube_file.write('POINT_DATA %s\n'%(self.xcount * self.ycount * self.zcount))
        cube_file.close()

    def __write_scalars(self, file_name):
        #
        cube_file = open(file_name, 'a')
        cube_file.write('SCALARS %s float 1\n'%self.property_name)
        cube_file.write('LOOKUP_TABLE default\n')
        for z in range(self.zcount):
            for y in range(self.ycount):
                for x in range(self.xcount):
                    cube_file.write('%f '%self.data_set[x,y,z])
                cube_file.write('\n')
        cube_file.close()

if __name__=='__main__':
    from mesh_tally import *
    test_dir = os.path.join('tests', 'cube')
    os.chdir(test_dir)

    cube_tally = meshTally('inp.tally','inp')
    cube_tally.setId(33)
    cube_writer = cubeWriter(cube_tally.getScope(), cube_tally.getData(), 'power', cube_tally.getBoundary())
    cube_writer.write('cube.vtk')
