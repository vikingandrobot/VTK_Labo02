#!/usr/bin/env python3

# This file contains the script to play the animation of the pieces
# of the puzzle solution

import sys
import vtk
from partials.shape_creation import createPieces
from partials.shape_creation import createOutlineCube
import numpy as np

# Callback to animate the pieces
class vtkTimerCallback():
    def __init__(self, pieces, vectors, duration, delta_t):
        self.pieces = pieces
        self.vectors = vectors
        self.duration = duration
        self.DELTA_T = delta_t
        self.INV_DELTA = delta_t / duration
        self.step = 0
        self.pieceIndex = 0

    def execute(self, obj, event):
        if (self.pieceIndex >= len(self.pieces)):
            return


        if (self.step < self.duration):
            i = 0
            shape = self.pieces[self.pieceIndex]
            v = [sub * -1 for sub in self.vectors[self.pieceIndex]]
            shape.SetPosition(
                shape.GetPosition()[0] + self.INV_DELTA * v[0],
                shape.GetPosition()[1] + self.INV_DELTA * v[1],
                shape.GetPosition()[2] + self.INV_DELTA * v[2],
            )
            i += 1

            self.step += self.DELTA_T
            iren = obj
            iren.GetRenderWindow().Render()
        else:
            self.pieceIndex = self.pieceIndex + 1
            self.step = 0

# Check number of arguments
if len(sys.argv) != 2:
    print("Please enter the input solution filename as argument.")
    print("Usage: python3 solution_multivue.py <input filename>")
    sys.exit(1)

# Read pieces ids from input text file
ids = np.genfromtxt(sys.argv[1], delimiter=' ', dtype=(int))

# Create pieces from ids
pieces = createPieces(ids)

# Here we compute the vectors to use to place the pieces outside of the cube
centerX = 1
centerY = 1
centerZ = 1

translateVectors = []

# For each piece
for piece in pieces:
    translateVector = [0, 0, 0]

    # We calculate a mean vector from each of the cube that make the piece
    for cubeActor in piece.GetParts():
        v = cubeActor.GetPosition()
        translateVector[0] += v[0] - centerX
        translateVector[1] += v[1] - centerY
        translateVector[2] += v[2] - centerZ

    translateVectors.append(translateVector)

# Normalize the vectors and multiply them by a constant factor
FACTOR = 3
norms = np.apply_along_axis(np.linalg.norm, 1, translateVectors)
for i in range(0, len(translateVectors)):
    for j in range(0, len(translateVectors[i])):
        translateVectors[i][j] = translateVectors[i][j] / norms[i] * FACTOR

# Move the pieces to its starting position using the vectors
for i in range(0, len(pieces)):
    piece = pieces[i]
    for cubeActor in piece.GetParts():
        cubeActor.SetPosition(cubeActor.GetPosition()[0] + translateVectors[i][0],
        cubeActor.GetPosition()[1] + translateVectors[i][1],
        cubeActor.GetPosition()[2] + translateVectors[i][2])


# Create the outline cube
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
renWin.SetSize(1280, 720)

# The vtkRenderWindowInteractor class watches for events (
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Invert the translating vectors

v = [[ele * -1 for ele in sub] for sub in translateVectors]
cb = vtkTimerCallback(pieces, translateVectors, 1000, 40)
iren.AddObserver('TimerEvent', cb.execute)
timerId = iren.CreateRepeatingTimer(40);

# Here we specify a particular interactor style.
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

ren.GetActiveCamera().SetPosition(0, 0, 20)
ren.GetActiveCamera().Azimuth(60)
ren.GetActiveCamera().Elevation(35)

renWin.Render()

# Initialize and start the event loop.
iren.Initialize()
iren.Start()
