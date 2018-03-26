#!/usr/bin/env python3

import sys
import vtk
from partials.shape_creation import createPieces
from numpy import genfromtxt

# Check number of arguments
if len(sys.argv) != 3:
    print("Please enter the input solution filename and the output filename as arguments.")
    print("Usage: python3 solution_multivue.py <input filename> <output filename>")
    sys.exit(1)

# Read pieces ids from input text file
ids = genfromtxt(sys.argv[1], delimiter=' ', dtype=(int))

# Create pieces from ids
pieces = createPieces(ids)

# Create renderers to display pieces one after another
renderers = []
for renNumber in range(0, 8):
    # Renderer viewport coordinates
    x = 0 if renNumber % 2 == 0 else 0.5
    y = (1 - 0.25 * (renNumber // 2)) - 0.25

    # Create a VtkRenderer and set its coordinates, background and add it
    # to our list
    ren = vtk.vtkRenderer()
    ren.SetViewport(x, y, x + 0.5, y + 0.25)
    ren.SetBackground(1, 1, 1)
    renderers.append(ren)

    # Add the cubes to the renderers
    if (renNumber > 0):
        for pieceNumber in range(0, renNumber):
            renderers[renNumber].AddActor(pieces[pieceNumber])

# outline
outlineCube = vtk.vtkCubeSource()
outlineCube.SetXLength(3)
outlineCube.SetYLength(3)
outlineCube.SetZLength(3)
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(outlineCube.GetOutputPort())
mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInputConnection(outline.GetOutputPort())
actor2 = vtk.vtkActor()
actor2.SetMapper(mapper2)
actor2.SetPosition(1, 1, 1)
actor2.GetProperty().SetColor(0, 0, 0)

# assign actor to the renderer
for renderer in renderers:
    renderer.AddActor(actor2)

# render window
renWin = vtk.vtkRenderWindow()
for ren in renderers:
    renWin.AddRenderer(ren)
# A4 format at 144 dpi
renWin.SetSize(1190, 1684)

# Set the same camera for every renderer
mainCamera = None
for renderer in renderers:
    if mainCamera is None:
        mainCamera = renderer.GetActiveCamera()
    else:
        renderer.SetActiveCamera(mainCamera)

# Set the camera to display pieces nicely
mainCamera.SetPosition(0, 2, 13)
mainCamera.Azimuth(45)
mainCamera.Elevation(20)

# The vtkRenderWindowInteractor class watches for events (
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Here we specify a particular interactor style.
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

renWin.Render()

# screenshot code:
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)
w2if.Update()

writer = vtk.vtkGL2PSExporter()
writer.SetFileFormatToPDF()
writer.SetFilePrefix(sys.argv[2])
writer.SetInput(renWin)
writer.Write()


# Initialize and start the event loop.
iren.Initialize()
iren.Start()
