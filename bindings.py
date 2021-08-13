# ctypes_test.py
import ctypes
import pathlib
from extra import STEP

WIDTH = 30
FILE = str(pathlib.Path().absolute() / "examples/demo.txt")

# Load the shared libraries into ctypes
libname = pathlib.Path().absolute() / "dynamic-map/clib.so"
clib = ctypes.CDLL(libname)


# print(map_lib.test(10, ctypes.c_float(2.3)));
# Check to make sure each .h file loaded
if clib.isPositionLoaded() == True:
    print("Position c++ library is loaded")
if clib.isMapLoaded() == True:
    print("Dynamic map c++ library is loaded")
if clib.isPathLoaded() == True:
    print("Path c++ library is loaded")

# Run the tests the .h files provide so we can make sure our bindings are good
# clib.pathTest.restype = array.astype(numpy.double)
clib.positionTest.restype = None
clib.positionTest.argtype = ctypes.POINTER(ctypes.c_int)
pos = []
pos = (ctypes.c_int * 2)(*pos)
clib.positionTest(pos)
if pos[:] == [2, 300]:
    print("Position c++ library is functional")

# Create a few good looking python-bound functions
MAP_PATH = "examples/maps/basic.txt"
PATH = []

clib.getPath.restype = None#ctypes.POINTER(ctypes.c_int)
clib.getPath.argtype = ctypes.POINTER(ctypes.c_int)
def _destroy(path):
    clib.destructor(path)

clib.getPath.restype = ctypes.POINTER(ctypes.c_int)
clib.getPath.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_wchar_p)
def findPath(start, end):
    global PATH
    print(str(pathlib.Path().absolute() / "examples/maps/basic.txt"))
    cpath = clib.getPath(round(start[0]), round(start[1]), round(end[0]), round(end[1]), STEP, FILE);
    i = cpath[0:1][0] + 1
    path = cpath[1:i]
    PATH = [(path[i], path[i+1]) for i in range(0, len(path), 2)]
    print(path, "PATH")
    path = []
    # Stop dem mem leaks
    _destroy(cpath)

def nextPosition():
    if len(PATH) == 0:
        return None
    return PATH.pop()

def hasPosition():
    if len(PATH) == 0:
        return False
    return True

# minor testing
findPath((0,0), (2,3));
while hasPosition():
    print(nextPosition())
