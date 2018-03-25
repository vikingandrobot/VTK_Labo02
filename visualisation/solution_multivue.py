#!/usr/bin/env python

import vtk
from shape_creation import createShapes
from numpy import genfromtxt

ids = genfromtxt('solution.txt', delimiter=' ', dtype=(int))
ids[:] = [[ele - 1 for ele in sub] for sub in ids]

# Create shapes from ids
shapes = createShapes(ids)

renderers = []
for renNumber in range(0, 8):
    # Renderer viewport coordinates
    x = 0 if renNumber % 2 == 0 else 0.5
    y = (1 - 0.25 * (renNumber // 2)) - 0.25

    # Create a VtkRenderer and set its coordinates, background and add it
    # to our list
    ren = vtk.vtkRenderer()
    ren.SetViewport(x, y, x + 0.5, y + 0.25)
    ren.SetBackground(0.95, 0.95, 0.95)
    renderers.append(ren)

    # Add the cubes to the renderers
    if (renNumber > 0):
        for shapeNumber in range(0, renNumber):
            for cube in shapes[shapeNumber]:
                renderers[renNumber].AddActor(cube)




centerX = 1
centerY = 1
centerZ = 1

transform = vtk.vtkTransform()
transform.Translate(-1.5, -1.5, -1.5)

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
# actor2.SetUserTransform(transform)

axes = vtk.vtkAxesActor()
#  The axes are positioned with a user transform
#axes.SetUserTransform(vtk.vtkTransform().Translate(12, -1, -1))
# assign actor to the renderer
for renderer in renderers:
    renderer.AddActor(actor2)
    renderer.AddActor(axes)
#
# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We also
# set the size to be 300 pixels by 300.
#
renWin = vtk.vtkRenderWindow()
for ren in renderers:
    renWin.AddRenderer(ren)
renWin.SetSize(1200, 1700)

# Set the same camera for every renderer
mainCamera = None
for renderer in renderers:
    if mainCamera is None:
        mainCamera = renderer.GetActiveCamera()
    else:
        renderer.SetActiveCamera(mainCamera)

mainCamera.SetPosition(0, 2, 13)
mainCamera.Azimuth(45)
mainCamera.Elevation(20)

#
# The vtkRenderWindowInteractor class watches for events (e.g., keypress,
# mouse) in the vtkRenderWindow. These events are translated into
# event invocations that VTK understands (see VTK/Common/vtkCommand.h
# for all events that VTK processes). Then observers of these VTK
# events can process them as appropriate.
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#
# By default the vtkRenderWindowInteractor instantiates an instance
# of vtkInteractorStyle. vtkInteractorStyle translates a set of events
# it observes into operations on the camera, actors, and/or properties
# in the vtkRenderWindow associated with the vtkRenderWinodwInteractor.
# Here we specify a particular interactor style.
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)


#
# Initialize and start the event loop. Once the render window appears, mouse
# in the window to move the camera. The Start() method executes an event
# loop which listens to user mouse and keyboard events. Note that keypress-e
# exits the event loop. (Look in vtkInteractorStyle.h for a summary of events,
# or the appropriate Doxygen documentation.)
#
iren.Initialize()
iren.Start()
