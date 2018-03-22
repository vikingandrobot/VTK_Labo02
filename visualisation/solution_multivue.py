#!/usr/bin/env python

import vtk
from shape_creation import createShapes
from numpy import genfromtxt


stages = genfromtxt('solution.txt', delimiter=' ', dtype = (int))


def createCubeActor(x, y, z):
    cube = vtk.vtkCubeSource()
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(cube.GetOutputPort())
    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(coneMapper)
    cubeActor.SetPosition([x, y, z])
    return cubeActor


def tShape():

    tShape = []

    for x in range(0, 4):
        cube = vtk.vtkCubeSource()
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(cube.GetOutputPort())
        cubeActor = vtk.vtkActor()
        cubeActor.SetMapper(coneMapper)
        tShape.append(cubeActor)

    tShape[0].SetPosition([0, 0, 0])
    tShape[1].SetPosition([1, 0, 0])
    tShape[2].SetPosition([2, 0, 0])
    tShape[3].SetPosition([1, 1, 0])

    return tShape


shapes = createShapes(stages)


ren1 = vtk.vtkRenderer()
ren1.SetBackground(0.95, 0.95, 0.95)



for shape in shapes:
    for cube in shape:
        ren1.AddActor(cube)

centerX = 1
centerY = 1
centerZ = 1

translateVectors = []

for shape in shapes:
    translateVector = [0, 0, 0]
    for cubeActor in shape:
        v = cubeActor.GetPosition()
        translateVector[0] += v[0] - centerX
        translateVector[1] += v[1] - centerY
        translateVector[2] += v[2] - centerZ

    for cubeActor in shape:
        cubeActor.SetPosition(cubeActor.GetPosition()[0] + translateVector[0],
        cubeActor.GetPosition()[1] + translateVector[1],
        cubeActor.GetPosition()[2] + translateVector[2])

    translateVectors.append(translateVector)

transform = vtk.vtkTransform()
transform.Translate(1.0, 1.0, 1.0)

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
#actor2.SetPosition(1, 1, 1)
actor2.GetProperty().SetColor(0, 0, 0)
actor2.SetUserTransform(transform)
# assign actor to the renderer
ren1.AddActor(actor2)

axes = vtk.vtkAxesActor()
#  The axes are positioned with a user transform
axes.SetUserTransform(transform)
# axes.SetXAxisLabelText('')
# axes.SetYAxisLabelText('')
# axes.SetZAxisLabelText('')


ren1.AddActor(axes)
#
# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We also
# set the size to be 300 pixels by 300.
#
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(1200, 800)

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
