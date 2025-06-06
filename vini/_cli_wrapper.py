#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from .viewer import Viff
from .pyqtgraph_vini.Qt import QtWidgets
from .Verboseprint import verboseprint
import os, sys

def main():
    parser = argparse.ArgumentParser(
        prog = "MR viewer",
        description = """ Visualize 2D/3D/4D images with python """
    )
    parser.add_argument("-i", "-in", "--input", metavar='N', nargs='+',
                        help = "specify input image to display",
                        type=str)
    parser.add_argument("-z", "--zmap", metavar='N', nargs='+',
                        help = "specify an overlay where two adjustable \
                        colorbars would liked to be displayed, e.g. zmap",
                        type=str)
    parser.add_argument("-f", "--func", "--functional", metavar='N', nargs='+',
                        help = "specify a functional image", type=str)
    parser.add_argument('-l', action='store_true', default=False,
                        dest='linked', help='Set linked views to true')

    parser.add_argument("files",nargs="*")

    args = parser.parse_args()

    filenames = args.input

    #override if empty
    if filenames is None:
        filenames = args.files

    z_filenames = args.zmap
    func_filenames = args.func
    is_linked = args.linked

    if filenames is None:
        filenames = []
    if z_filenames is None:
        z_filenames = []
    if func_filenames is None:
        func_filenames = []
        
        
        

    # Initialize QT app GUI and setup the layout.
    app = QtWidgets.QApplication([])
    viewer = Viff()

    # change order of the images being loaded to be more intuitive
    filenames.reverse()
    z_filenames.reverse()
    func_filenames.reverse()

    if is_linked:
        viewer.is_linked = True
        file_list = []
        type_list = []
        if filenames is not None:
            for i in range(0, len(filenames)):
                verboseprint("Loading file: " + filenames[i])
                if os.path.isfile(filenames[i]):
                    file_list.append(filenames[i])
                    type_list.append(0)
                else:
                    print("Error: File doesn't exist")
        if z_filenames is not None:
            for i in range(0, len(z_filenames)):
                verboseprint("Loading file: " + z_filenames[i])
                if os.path.isfile(z_filenames[i]):
                    file_list.append(z_filenames[i])
                    type_list.append(1)
                else:
                    print("Error: File doesn't exist")
        if func_filenames is not None:
            for i in range(0, len(func_filenames)):
                verboseprint("Loading file: " + func_filenames[i])
                if os.path.isfile(func_filenames[i]):
                    file_list.append(func_filenames[i])
                    type_list.append(2)
                else:
                    print("Error: File doesn't exist")
        if file_list is not None:
            viewer.loadImagesFromFiles(file_list, type_list)
        viewer.checkIf2DAndRemovePanes()
        len_files = len(filenames)
        len_funcs = len(func_filenames)
        len_zmaps = len(z_filenames)

        # now open new windows and move the z-maps and functional images there
        for i in range(1, len_zmaps + len_funcs):
            verboseprint("move image to new window")
            viewer.newWindowInd(i) # adds to new window
            viewer.deactivateImageIndex(i) # remove from main window

        for i in range(len_zmaps + len_funcs, len_files + len_zmaps +
                len_funcs):
            for j in range(1, len(z_filenames + func_filenames)):
                verboseprint("move underlay to new window")
                viewer.addToWindowId(i,j-1)

    else:
        file_list = []
        type_list = []
        if filenames is not None:
            for i in range(0, len(filenames)):
                verboseprint("Loading file: " + filenames[i])
                if os.path.isfile(filenames[i]):
                    file_list.append(filenames[i])
                    type_list.append(0)
                else:
                    print("Error: File doesn't exist: {}".format(filenames[i]))
        if z_filenames is not None:
            for i in range(0, len(z_filenames)):
                verboseprint("Loading file: " + z_filenames[i])
                if os.path.isfile(z_filenames[i]):
                    file_list.append(z_filenames[i])
                    type_list.append(1)
                else:
                    print("Error: File doesn't exist: {}".format(filenames[i]))
        if func_filenames is not None:
            for i in range(0, len(func_filenames)):
                verboseprint("Loading file: " + func_filenames[i])
                if os.path.isfile(func_filenames[i]):
                    file_list.append(func_filenames[i])
                    type_list.append(2)
                else:
                    print("Error: File doesn't exist: {}".format(filenames[i]))
        if file_list is not None:
            viewer.loadImagesFromFiles(file_list, type_list)
            
    sys.exit(app.exec())