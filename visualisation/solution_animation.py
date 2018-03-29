#!/usr/bin/env python3

# This file contains the script to play the animation of the pieces
# of the puzzle solution. The program plays the animation in a window,
# and saves the animation to a .avi file which name is specified by the user.
# Fun fact: if you move the camera while rendering, the output file will also
# be affected. You can now let your creativity speak and customize the
# rendering of the animation (amazing!)

import sys
import vtk
from partials.shape_creation import createPieces
from partials.shape_creation import createOutlineCube
import numpy as np


# Callback to animate the pieces. It moves the pieces to their position in
# the cube one by one, saving a frame to the video output file each time.
# When the animation is complete, it ends the program
class vtkTimerCallback():
    def __init__(self, pieces, vectors, writer, w2if, duration, delta_t):
        self.pieces = pieces
        self.vectors = vectors
        self.writer = writer
        self.w2if = w2if
        self.duration = duration
        self.DELTA_T = delta_t
        self.INV_DELTA = delta_t / duration
        self.step = 0
        self.pieceIndex = 0

    def execute(self, obj, event):
        iren = obj
        if (self.pieceIndex >= len(self.pieces)):
            writer.End()
            iren.GetRenderWindow().Finalize();
            iren.TerminateApp();
            return

        if (self.step < self.duration):
            shape = self.pieces[self.pieceIndex]
            position = shape.GetPosition()
            v = self.vectors[self.pieceIndex]
            shape.SetPosition(
                position[0] + self.INV_DELTA * v[0],
                position[1] + self.INV_DELTA * v[1],
                position[2] + self.INV_DELTA * v[2],
            )

            # Update the step
            self.step += self.DELTA_T

            # Render the window and save the video
            iren.GetRenderWindow().Render()
            self.w2if.Modified()
            self.writer.Write()
        else:
            self.pieceIndex = self.pieceIndex + 1
            self.step = 0


# Check number of arguments
if len(sys.argv) != 3:
    print("Please enter the input solution filename and the output filename as arguments.")
    print("Usage: python3 solution_multivue.py <input filename> <output filename>")
    sys.exit(1)

# Read pieces ids from input text file
ids = np.genfromtxt(sys.argv[1], delimiter=' ', dtype=(int))

# Create pieces from ids
pieces = createPieces(ids)

# Here we compute the vectors to use to place the pieces outside of the cube
centerX = 1
centerY = 1
centerZ = 1

# The translation vector to use to animate the pieces
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

# Move the pieces to their starting position using the vectors
for i in range(0, len(pieces)):
    piece = pieces[i]
    for cubeActor in piece.GetParts():
        position = cubeActor.GetPosition()
        cubeActor.SetPosition(position[0] + translateVectors[i][0],
        position[1] + translateVectors[i][1],
        position[2] + translateVectors[i][2])


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

# Invert the translation vectors
v = [[ele * -1 for ele in sub] for sub in translateVectors]

# Here we specify a particular interactor style.
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

ren.GetActiveCamera().SetPosition(0, 0, 20)
ren.GetActiveCamera().Azimuth(60)
ren.GetActiveCamera().Elevation(35)

renWin.Render()

# Create resources to export the video
windowToImageFilter = vtk.vtkWindowToImageFilter()
windowToImageFilter.SetInput(renWin)
windowToImageFilter.Update()

writer = vtk.vtkOggTheoraWriter()
writer.SetInputConnection(windowToImageFilter.GetOutputPort())
writer.SetFileName(sys.argv[2] + ".avi")
writer.SetRate(25)
writer.Start()

# Register the callback for the animation
cb = vtkTimerCallback(pieces, v, writer, windowToImageFilter, 1000, 40)
iren.AddObserver('TimerEvent', cb.execute)
timerId = iren.CreateRepeatingTimer(40);

# Initialize and start the event loop.
iren.Initialize()
iren.Start()
