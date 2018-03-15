#!/usr/bin/env python

import vtk

COLORS = [
    [35, 61, 77],
    [254, 127, 45],
    [252, 202, 70],
    [161, 193, 129],
    [97, 155, 138],
    [40, 175, 176],
    [221, 206, 205]
]
COLORS[:] = [[ele / 255 for ele in sub] for sub in COLORS]

stages = [
    [3, 0, 0, 2, 2, 2, 1, 1, 1],
    [3, 5, 0, 3, 5, 2, 3, 1, 4],
    [6, 6, 0, 6, 5, 4, 6, 5, 4]
]


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


def shapeTranslatePosition(shape, x, y, z):
    for actor in shape:
        actor.SetPosition([actor.GetPosition()[0] + x, actor.GetPosition()[1] + y, actor.GetPosition()[2] + z])


shapes = [
    [],
    [],
    [],
    [],
    [],
    [],
    []
]


ren1 = vtk.vtkRenderer()
ren1.SetBackground(0.95, 0.95, 0.95)

for stageNumber in range(0, 3):
    for cubeNumber in range(0, 9):
        figureNumber = stages[stageNumber][cubeNumber]
        cube = createCubeActor(cubeNumber % 3, cubeNumber // 3, stageNumber)
        cube.GetProperty().SetColor(COLORS[figureNumber][0], COLORS[figureNumber][1], COLORS[figureNumber][2])
        shapes[figureNumber].append(cube)

for shape in shapes:
    for cube in shape:
        ren1.AddActor(cube)

# cube.SetXLength(1.0)
# cube.SetYLength(1.0)
# cube.SetZLength(1.0)

#
# In this example we terminate the pipeline with a mapper process object.
# (Intermediate filters such as vtkShrinkPolyData could be inserted in
# between the source and the mapper.)  We create an instance of
# vtkPolyDataMapper to map the polygonal data into graphics primitives. We
# connect the output of the cone souece to the input of this mapper.
#
# coneMapper = vtk.vtkPolyDataMapper()
# coneMapper.SetInputConnection(cube.GetOutputPort())

#
# Create an actor to represent the cone. The actor orchestrates rendering of
# the mapper's graphics primitives. An actor also refers to properties via a
# vtkProperty instance, and includes an internal transformation matrix. We
# set this actor's mapper to be coneMapper which we created above.
#

# tShape1 = tShape()
# shapes.append(tShape1)
# tShape2 = tShape()
# shapes.append(tShape2)
# shapeTranslatePosition(tShape2, 0, 0, 1)


# ren1 = vtk.vtkRenderer()
# ren1.SetBackground(0.95, 0.95, 0.95)

# i = 0
# for shape in shapes:
#     for cubeActor in shape:
#         cubeActor.GetProperty().SetColor(COLORS[i][0], COLORS[i][1], COLORS[i][2])
#         ren1.AddActor(cubeActor)
#     i += 1


#
# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We also
# set the size to be 300 pixels by 300.
#
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(600, 600)

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
# Unlike the previous scripts where we performed some operations and then
# exited, here we leave an event loop running. The user can use the mouse
# and keyboard to perform the operations on the scene according to the
# current interaction style.
#

#
# Initialize and start the event loop. Once the render window appears, mouse
# in the window to move the camera. The Start() method executes an event
# loop which listens to user mouse and keyboard events. Note that keypress-e
# exits the event loop. (Look in vtkInteractorStyle.h for a summary of events,
# or the appropriate Doxygen documentation.)
#
iren.Initialize()
iren.Start()
