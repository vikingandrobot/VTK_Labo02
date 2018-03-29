#!/usr/bin/env python

# Author: Mathieu Monteverde
# Date: 29.03.2018
# File: shape_creation.py

# This file contains the function to create the pieces needed in both scripts
# to render solutions and to animate them.
# It also contains the function to create the cube container outline

import vtk
from partials.colors import COLORS


# Create a cube actor at the (x, y, z) position
def createCubeActor(x, y, z):
    cube = vtk.vtkCubeSource()
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cube.GetOutputPort())
    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(coneMapper)
    cubeActor.SetPosition([x, y, z])
    return cubeActor


# Create the shapes using an array of pieces ids.
# The pieces are ordered following the increasing x axis.
def createPieces(ids):
    # A dictionary giving the pieces index in the list by Id
    indexDict = {}
    # List of pieces
    pieces = []
    # Current index
    index = 0

    # We parse the Id from x to y to z in order to have the most enjoyable
    # piece order when rendering. Back pieces first and front pieces last
    for x in range(0, 3):
        for y in range(0, 3):
            for z in range(0, 3):

                # Position in the array
                stageNumber = z
                cubeNumber = x + (3 * y)

                # Figure ID from the array
                pieceId = ids[z][cubeNumber]

                # Complete the dictionary of ids indexes
                if pieceId not in indexDict:
                    indexDict[pieceId] = index
                    # Create the vtlAssembly of the current cube
                    pieces.append(vtk.vtkAssembly())
                    index += 1

                # The index of the current shape
                pieceIndex = indexDict[pieceId]

                # Create the cube, set its color, and add it to the list of
                # pieces
                cube = createCubeActor(cubeNumber % 3, cubeNumber // 3,
                    stageNumber)
                cube.GetProperty().SetColor(COLORS[pieceIndex][0],
                    COLORS[pieceIndex][1], COLORS[pieceIndex][2])
                pieces[pieceIndex].AddPart(cube)

    return pieces


# Create the outline cube
# From the example here : https://www.vtk.org/Wiki/VTK/Examples/Cxx/PolyData/Outline
def createOutlineCube():
    # Source cube of size 3
    outlineCube = vtk.vtkCubeSource()
    outlineCube.SetXLength(3)
    outlineCube.SetYLength(3)
    outlineCube.SetZLength(3)
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(outlineCube.GetOutputPort())
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(outline.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Center and black
    actor.SetPosition(1, 1, 1)
    actor.GetProperty().SetColor(0, 0, 0)
    return actor
