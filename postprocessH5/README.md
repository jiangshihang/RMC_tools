# Function of this script:
Read desired data from .h5 file,  
and write the data to tecplot .dat file.

# Usage of this script:
You need to prepare two inp file:
- **map**: map of the core. The map needs to be square. Position is marked with 0 if there is no assembly; otherwise it's marked by 1. For example:  
0 1 0  
1 1 1  
0 1 0  
presents a core with five assemblies.
- **h5_config**: configuration file. Two parameters are necessary for now:
  - hdf5name: name of the hdf5 file
  - dataset: name of the desired dataset
