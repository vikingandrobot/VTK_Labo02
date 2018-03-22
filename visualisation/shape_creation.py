#!/usr/bin/env python

import vtk
from colors import COLORS


def createCubeActor(x, y, z):
    cube = vtk.vtkCubeSource()
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cube.GetOutputPort())
    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(coneMapper)
    cubeActor.SetPosition([x, y, z])
    return cubeActor


def createShapes(ids):
    shapes = [[], [], [], [], [], [], []]

    for stageNumber in range(0, 3):
        for cubeNumber in range(0, 9):
            figureNumber = ids[stageNumber][cubeNumber]
            cube = createCubeActor(cubeNumber % 3, cubeNumber // 3, stageNumber)
            cube.GetProperty().SetColor(COLORS[figureNumber][0], COLORS[figureNumber][1], COLORS[figureNumber][2])
            shapes[figureNumber].append(cube)

    return shapes
