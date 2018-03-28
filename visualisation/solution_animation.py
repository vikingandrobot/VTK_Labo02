#!/usr/bin/env python3

import sys
import vtk
from partials.shape_creation import createPieces
from partials.shape_creation import createOutlineCube
from numpy import *

class vtkTimerCallback():
    def __init__(self):
        self.delta = 25 / 2000
        self.step = 0
        self.pieceIndex = 0

    def execute(self, obj, event):
        if (self.pieceIndex >= len(self.shapes)):
            return


        if (self.step < 2000):
            i = 0
            shape = self.shapes[self.pieceIndex]
            v = [sub * -1 for sub in self.vectors[self.pieceIndex]]
            shape.SetPosition(
                shape.GetPosition()[0] + self.delta * v[0],
                shape.GetPosition()[1] + self.delta * v[1],
                shape.GetPosition()[2] + self.delta * v[2],
            )
            i += 1

            self.step += 25
            iren = obj
            iren.GetRenderWindow().Render()
        else:
            self.pieceIndex = self.pieceIndex + 1
            self.step = 0

# Check number of arguments
if len(sys.argv) != 3:
    print("Please enter the input solution filename and the output filename as arguments.")
    print("Usage: python3 solution_multivue.py <input filename> <output filename>")
    sys.exit(1)

# Read pieces ids from input text file
ids = genfromtxt(sys.argv[1], delimiter=' ', dtype=(int))

# Create pieces from ids
pieces = createPieces(ids)


centerX = 1
centerY = 1
centerZ = 1


translateVectors = []

for shape in pieces:
    translateVector = [0, 0, 0]
    for cubeActor in shape.GetParts():
        v = cubeActor.GetPosition()
        translateVector[0] += v[0] - centerX
        translateVector[1] += v[1] - centerY
        translateVector[2] += v[2] - centerZ

    # for cubeActor in shape.GetParts():
    #     cubeActor.SetPosition(cubeActor.GetPosition()[0] + translateVector[0],
    #     cubeActor.GetPosition()[1] + translateVector[1],
    #     cubeActor.GetPosition()[2] + translateVector[2])

    translateVectors.append(translateVector)

norms = apply_along_axis(linalg.norm, 1, translateVectors)
for i in range(0, len(translateVectors)):
    for j in range(0, len(translateVectors[i])):
        translateVectors[i][j] = translateVectors[i][j] / norms[i] * 4

for i in range(0, len(pieces)):
    shape = pieces[i]
    for cubeActor in shape.GetParts():
        cubeActor.SetPosition(cubeActor.GetPosition()[0] + translateVectors[i][0],
        cubeActor.GetPosition()[1] + translateVectors[i][1],
        cubeActor.GetPosition()[2] + translateVectors[i][2])



outlineCube = createOutlineCube()

# Renderer
ren = vtk.vtkRenderer()
ren.SetBackground(1, 1, 1)
for piece in pieces:
    ren.AddActor(piece)
ren.AddActor(outlineCube)

# Window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(1190, 1684)

# The vtkRenderWindowInteractor class watches for events (
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

cb = vtkTimerCallback()
cb.shapes = pieces
cb.vectors = translateVectors
iren.AddObserver('TimerEvent', cb.execute)
timerId = iren.CreateRepeatingTimer(25);

# Here we specify a particular interactor style.
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

renWin.Render()

ren.GetActiveCamera().Azimuth(45)
ren.GetActiveCamera().Elevation(20)

# Initialize and start the event loop.
iren.Initialize()
iren.Start()
