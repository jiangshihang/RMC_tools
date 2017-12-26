#! /usr/bin/python
# -*- coding=utf-8 -*-
import os
import sys
from optparse import OptionParser
from mesh_tally import *
from cube import *
from cylinder import *

os.chdir(sys.path[0])

def main():

    usage="""usage: %prog [options]"""
    parser = OptionParser(usage=usage)
    parser.add_option('-g', '--geo', dest='geo', default='mesh',\
                      help='Geometry type, choose from mesh or rod. Default: mesh.')
    parser.add_option('-i', '--input', dest='inp', default='inp',\
                      help='Name of the input card. Default: inp.')
    parser.add_option('-t', '--tally', dest='tally', default='inp.tally',\
                      help='Name of the tally. Default: inp.tally')
    parser.add_option('-s', '--resolution', dest='resolution', default='6',\
                      help='Value of the resolution, only valid for rod geometry. Default: 6.')
    parser.add_option('-d', '--id', dest='id', default='1',\
                      help='Id number. Default: 1.')
    parser.add_option('-p', '--property', dest='property', default='power',\
                      help='Property of the value. Default: power.')
    parser.add_option('-o', '--out', dest='out', default='inp.vtk',\
                      help='Output file name. Default: inp.vtk')

    (options, args) = parser.parse_args()

    tally_file_name = options.tally
    inp_file_name = options.inp
    resolution = int(options.resolution)
    idnum = int(options.id)
    property_name = options.property
    out_file_name = options.out

    tally = meshTally(tally_file_name, inp_file_name)
    tally.setId(idnum)

    if options.geo == 'mesh':
        cube_writer = cubeWriter(tally.getScope(), tally.getData(), property_name, tally.getBoundary())
        cube_writer.write(out_file_name)
    elif options.geo == 'rod':
        cylinder_writer = cylinderWriter(tally.getScope(), tally.getData(), property_name, resolution, tally.getBoundary())
        cylinder_writer.write(out_file_name)
        
if __name__=='__main__':
    main()