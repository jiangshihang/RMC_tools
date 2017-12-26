# -*- coding=utf-8 -*-
import math

class cylinderWriter:
    '''

    '''
    def __init__(self, scope, data_set, property_name, resolution, boundary, radius = 0 ):
        #
        [self.xcount, self.ycount, self.zcount] = scope
        self.data_set = data_set
        self.property_name = property_name

        self.resolution = resolution
        [self.xbound, self.ybound, self.zbound] = boundary
        
        self.xstep = (self.xbound[1]-self.xbound[0])/self.xcount
        self.ystep = (self.ybound[1]-self.ybound[0])/self.ycount
        self.zstep = (self.zbound[1]-self.zbound[0])/self.zcount

        if radius == 0:
            self.radius = min(self.xstep, self.ystep, self.zstep)/3
        else:
            self.radius = radius

        self.coords = np.empty(self.xcount*self.ycount*self.zcount*3).reshape(self.xcount,self.ycount,self.zcount,3)
        for z in range(self.zcount):
            for y in range(self.ycount):
                for x in range(self.xcount):
                    self.coords[x,y,z,0] = self.xbound[0] + (x+0.5)*self.xstep
                    self.coords[x,y,z,1] = self.ybound[0] + (y+0.5)*self.ystep
                    self.coords[x,y,z,2] = self.zbound[0] + (z+0.5)*self.zstep

    def write(self, file_name):
        # 
        cylinder_file = open(file_name, 'w')
        cylinder_file.write('# vtk DataFile Version 2.0\n')
        cylinder_file.write('Rod Data\n')
        cylinder_file.write('ASCII\n')
        cylinder_file.write('DATASET UNSTRUCTURED_GRID\n')
        cylinder_file.close()
        self.__write_points(file_name)
        self.__write_cells(file_name)
        self.__write_cell_types(file_name)
        self.__write_lookuptable(file_name)

    def __write_points(self, file_name):
        #
        cylinder_file = open(file_name, 'a')
        cylinder_file.write('POINTS %s double\n'%(6 * self.resolution * self.xcount * self.ycount * self.zcount))
        for z in range(self.zcount):
            for y in range(self.ycount):
                for x in range(self.xcount):
                    for res in range(self.resolution):
                        cylinder_file.write(' %.6E %.6E %.6E\n'%(self.coords[x,y,z,0],\
                                                                 self.coords[x,y,z,1],\
                                                                 self.coords[x,y,z,2]+self.zstep/2))
                        cylinder_file.write(' %.6E %.6E %.6E\n'%(self.coords[x,y,z,0]+self.radius*math.cos(res*2*math.pi/self.resolution),\
                                                                 self.coords[x,y,z,1]+self.radius*math.sin(res*2*math.pi/self.resolution),\
                                                                 self.coords[x,y,z,2]+self.zstep/2))
                        cylinder_file.write(' %.6E %.6E %.6E\n'%(self.coords[x,y,z,0]+self.radius*math.cos((res+1)*2*math.pi/self.resolution),\
                                                                 self.coords[x,y,z,1]+self.radius*math.sin((res+1)*2*math.pi/self.resolution),\
                                                                 self.coords[x,y,z,2]+self.zstep/2))
                        cylinder_file.write(' %.6E %.6E %.6E\n'%(self.coords[x,y,z,0],\
                                                                 self.coords[x,y,z,1],\
                                                                 self.coords[x,y,z,2]-self.zstep/2))
                        cylinder_file.write(' %.6E %.6E %.6E\n'%(self.coords[x,y,z,0]+self.radius*math.cos(res*2*math.pi/self.resolution),\
                                                                 self.coords[x,y,z,1]+self.radius*math.sin(res*2*math.pi/self.resolution),\
                                                                 self.coords[x,y,z,2]-self.zstep/2))
                        cylinder_file.write(' %.6E %.6E %.6E\n'%(self.coords[x,y,z,0]+self.radius*math.cos((res+1)*2*math.pi/self.resolution),\
                                                                 self.coords[x,y,z,1]+self.radius*math.sin((res+1)*2*math.pi/self.resolution),\
                                                                 self.coords[x,y,z,2]-self.zstep/2))
        cylinder_file.close()

    def __write_cells(self, file_name):
        #
        cell_num = self.resolution*self.xcount*self.ycount*self.zcount

        cylinder_file = open(file_name, 'a')
        cylinder_file.write('CELLS %s %s\n'%(cell_num, cell_num*7))

        for cell in range(cell_num):
            cylinder_file.write(' 6 %s %s %s %s %s %s\n'%(cell*6+0, cell*6+1, cell*6+2, cell*6+3, cell*6+4, cell*6+5))

        cylinder_file.close()

    def __write_cell_types(self, file_name):
        #
        cell_num = self.resolution*self.xcount*self.ycount*self.zcount

        cylinder_file = open(file_name, 'a')
        cylinder_file.write('CELL_TYPES %s\n'%cell_num)
        for cell in range(cell_num):
            cylinder_file.write('13\n')

        cylinder_file.write('CELL_DATA %s\n'%cell_num)

        cylinder_file.close()

    def __write_lookuptable(self, file_name):
        #
        cylinder_file = open(file_name, 'a')
        cylinder_file.write('SCALARS %s float\n'%self.property_name)
        cylinder_file.write('LOOKUP_TABLE default\n')
        for z in range(self.zcount):
            for y in range(self.ycount):
                for x in range(self.xcount):
                    for res in range(self.resolution):
                        cylinder_file.write('%s '%self.data_set[x,y,z])
                    cylinder_file.write('\n')

        cylinder_file.close()

if __name__=='__main__':
    #
    import numpy as np
    from mesh_tally import *

    test_dir = os.path.join('tests', 'cylinder')
    os.chdir(test_dir)

    cylinder_tally = meshTally('inp.tally', 'inp')
    cylinder_tally.setId(39)
    cylinder_writer = cylinderWriter(cylinder_tally.getScope(), cylinder_tally.getData(), 'power', 6, cylinder_tally.getBoundary(), 0.06)
    cylinder_writer.write('cylinder9.vtk')