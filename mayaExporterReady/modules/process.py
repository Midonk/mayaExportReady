# coding=utf-8

import maya.cmds as cmds
import os
import ui_manager as ui
import utility
from mayaExporterReady import storage

fileExists = cmds.file(storage.scene, q=True, exists=True)
fileModified = cmds.file(storage.scene, q=True, modified=True)


# Manage the save process following the scene state
def saveScene():
    global fileExists
    if not fileExists:
        # The file has already a name
        if storage.scene != "":
            cmds.file(save=True)

        # the file need a name => then a location
        else:
            scene = cmds.fileDialog2(ds=2, fm=0)
            if scene is not None:
                storage.scene = scene[0]
                sceneName = os.path.splitext(os.path.basename(storage.scene))[0]
                storage.scene = cmds.file(rename=os.path.join(os.path.dirname(storage.scene), sceneName + ".ma"))
                cmds.file(save=True, type='mayaAscii')
                print("scene saved as " + storage.scene)

            # The user canceled the dialog
            else:
                if storage.values.displayInfo:
                    ui.info("Warning", "The script can't continue without saving")
                print("\nEnd of script\n")

    elif fileModified:
        cmds.file(save=True)

    fileExists = True


# Check the scene state
def checkSave():
    # check if the scene exists in the os or if it has been modified
    if not fileExists or fileModified:
        if ui.confirm("Save scene",
                      "You need to save your scene before using this script\n\nDo you want to save your scene now ?\n"):

            saveScene()
            return True

        # The user canceled the modal
        else:
            print("\nEnd of script\n")
            return False

    return True


# Check if the opened scene is an export file
def checkExportFile(sceneName):
    if "_export" in storage.sceneName:
        # The user canceled the modal
        if not ui.confirm("File duplication",
                          "It seems the open scene is already an export file.\n"
                          "\nAre you sure you want to run the script on this scene ?\n"):
            print("\nEnd of script\n")
            return False

    return True


# Check if there is already an existing export file of the opened scene
def checkDuplication(scene):
    # if the user doesn't want to override the existing export file and that an export file of the opened scene exists
    if not storage.values.alwaysOverrideExport and cmds.file(scene, q=True, exists=True):
        # The user canceled the modal
        if not ui.confirm("Override export file",
                          "An export file of this scene may already exist.\n\nDo you want to override it ?"):
            print("\nEnd of script\n")
            return False

    return True


# Split transform nodes between meshes and otherElement
def splitTransform(transformNodes):
    for node in transformNodes:
        if cmds.objExists(node):
            storage.transformNodes.append(node)
            if utility.isMesh(node):
                storage.meshes.append(node)

            else:
                storage.otherElement.append(node)

    # print("transformNodes", storage.transformNodes)
    # print("meshes", storage.meshes)
    # print("otherElement", storage.otherElement)


# Rebuild normals
def rebuildNormals():
    for mesh in storage.meshes:
        # Rebuild in classic soft edge
        if storage.values.rebuildNormalOption == 1:
            cmds.polySoftEdge(mesh, a=30)

        # Rebuild in hard edge
        elif storage.values.rebuildNormalOption == 2:
            cmds.polySoftEdge(mesh, a=0)

        # Rebuild with a custom angle (till 180)
        elif storage.values.rebuildNormalOption == 3:
            cmds.polySoftEdge(mesh, a=storage.values.customNormalAngle)


# Set the pivot point following user choice
def setPivot():
    # center pivot on mesh
    if storage.values.pivotOption == 2:
        if storage.values.displayInfo:
            ui.info("Info", "The script set the pivot of your mesh at the center of them")
        for mesh in storage.meshes:
            cmds.xform(mesh, r=True, centerPivots=True)

    # center pivot on scene
    elif storage.values.pivotOption == 3:
        if storage.values.displayInfo:
            ui.info("Info", "The script set the pivot of your mesh at the center of scene")
        for mesh in storage.meshes:
            cmds.xform(mesh, ws=True, pivots=[0, 0, 0])

    # center pivot on mesh base
    elif storage.values.pivotOption == 4:
        if storage.values.displayInfo:
            ui.info("Info", "The script set the pivot of your mesh at the center of the bottom of your mesh")
        for mesh in storage.meshes:
            cmds.xform(mesh, r=True, centerPivots=True)
            pivotPos = cmds.xform(mesh, q=True, pivots=True, ws=True)

            # Get vtx pos from  Narann => https://www.fevrierdorian.com/blog/post/2011/09/27/Quickly-retrieve-vertex-positions-of-a-Maya-mesh-%28English-Translation%29
            vtxWorldPosition = []
            vtxIndexList = cmds.getAttr(mesh + ".vrts", multiIndices=True)
            for i in vtxIndexList:
                curPointPosition = cmds.xform(mesh + ".pnts[" + str(i) + "]", q=True, t=True, ws=True)
                vtxWorldPosition.append(curPointPosition)
            # end of Narann code

            # get the lowest vertex Y transform at first
            vtxWorldPosition.sort(key=lambda e: e[1])
            cmds.xform(mesh, ws=True, pivots=[pivotPos[0], vtxWorldPosition[0][1], pivotPos[2]])


# Look for non-manyfold meshes
def checkNonManyfold():
    probMesh = []
    for mesh in storage.meshes:
        nme = cmds.polyInfo(mesh, nme=True)
        nue = cmds.polyInfo(mesh, nue=True)
        nuv = cmds.polyInfo(mesh, nuv=True)
        nmv = cmds.polyInfo(mesh, nmv=True)

        if nme is not None or nue is not None or nuv is not None or nmv is not None:
            probMesh.append(mesh)
            print(mesh + ":")
            print(" Non-manifold Edges", nme)
            print(" Non-manifold Vertices", nmv)
            print(" Non-manifold UV Edges", nue)
            print(" Non-manifold UVs", nuv)

    return probMesh


# Export the objects following parameter
def exportObjects(destDir, name, asOne=False):
    if storage.values.exportExtension == "exportFbx":
        cmds.loadPlugin('fbxmaya.mll', quiet=True)
        cmds.file(destDir + "\\" + name, force=True, options="v = 0", type="FBX export", exportAll=asOne,
                  exportSelected=not asOne)

    else:
        cmds.loadPlugin('objExport.mll', quiet=True)
        cmds.file(destDir + "\\" + name, force=True, type="OBJexport", exportSelected=not asOne, exportAll=asOne)


# Prepare and redirect the objects to the correct export type
def prepareExport(defaultName, customName):
    # base destDir
    destDir = storage.values.exportFolder
    generatedElement = defaultName if customName == "" else customName
    # create folder if there are multiple elements
    if not storage.values.exportAsOneObject:
        destDir += "\\" + generatedElement

        if not cmds.file(destDir, q=True, exists=True):
            cmds.sysFile(destDir, makeDir=True)

    if storage.values.displayInfo:
        ui.info("Info",
                "The script export your scene as individual meshes and stores them into:\n" + "'" + destDir + "'")

    # Export meshes
    if not storage.values.exportAsOneObject:
        for mesh in storage.meshes:
            cmds.select(clear=True)
            cmds.select(mesh, add=True)
            exportObjects(destDir, mesh)

    # as one object
    else:
        exportObjects(destDir, generatedElement, True)


"""
app definition
"""


def mayaExporterReady():
    print('\nLancement du script\n')

    cmds.undoInfo(cn="mayaExporterReady", ock=True)
    # Aware the user of what it will happen
    if storage.values.displayInfo:
        ui.info("Info",
                "The script will now proceed through several operations, as you parametered it in the preceding window")

    # Getting all transformNodes needed
    if storage.values.displayInfo:
        ui.info("Info", "The script gather all the transformNodes of the scene to prepare them to the export")

    # Store meshes following the options
    if not storage.values.selectionOnly:
        cmds.select(all=True, hierarchy=True)

    selectedMeshes = cmds.ls(sl=True, type="transform")

    # """""""""""""

    #  CHECK FILES

    # """""""""""""

    storage.scene = storage.scene = cmds.file(q=True, sn=True)

    # check the localization of the file
    storage.scene = cmds.file(q=True, sn=True)

    if not checkSave():
        return

    storage.sceneName, storage.sceneExt = os.path.splitext(os.path.basename(storage.scene))

    # check if the file is not an export file
    if not checkExportFile(storage.sceneName):
        return

    # Check if there is no duplicated project
    sceneCopy = os.path.join(os.path.dirname(storage.scene), storage.sceneName + "_export" + storage.sceneExt)

    if storage.values.displayInfo:
        ui.info("Info", "The script is now checking for an existing export file generated earlier")

    if not checkDuplication(sceneCopy):
        return

    # Duplicate the project
    if storage.values.displayInfo:
        ui.info("Info", "The script duplicate your scene as an 'export' file")

    cmds.sysFile(storage.scene, copy=sceneCopy)

    # Opening of the new project into Maya
    if storage.values.displayInfo:
        ui.info("Info", "The script is opening the duplicated scene in Maya")

    # We need to save the scene to save the metadata modified
    cmds.file(save=True)
    cmds.file(sceneCopy, open=True)

    # """""""""""""""""""""

    #  PREPARE THE PROCESS

    # """""""""""""""""""""

    # First delete history of the transforms
    for node in selectedMeshes:
        cmds.delete(node, constructionHistory=True)

    # Splitting into meshes and otherElement
    splitTransform(selectedMeshes)

    # Make sure that at least one mesh or group is selected
    if len(storage.transformNodes) == 0:
        ui.info("Error", "No mesh or group detected in your scene")
        cmds.file(storage.scene, force=True, open=True)
        print('\nFin du script\n')
        return

    if storage.values.displayInfo:
        ui.info("Info", "The script is ready to prepare your transformNodes")

    # """""""""

    #  PROCESS

    # """""""""

    # conform normals
    if storage.values.conformNormals:
        if storage.values.displayInfo:
            ui.info("Info", "The script conform the normals of your transformNodes as you asked for")

        for mesh in storage.meshes:
            cmds.polyNormal(mesh, nm=2)

    # Rebuild normals
    if storage.values.rebuildNormals:
        if storage.values.displayInfo:
            ui.info("Info",
                    "The script rebuild the normals of your transformNodes as you asked for, with parameter " + str(
                        storage.values.rebuildNormalOption))

        rebuildNormals()

    # set pivot of the mesh
    setPivot()

    # clean up
    if storage.values.cleanUpMesh:
        if storage.values.displayInfo:
            ui.info("Info", "The script is cleaning your mesh")

        for mesh in storage.meshes:
            cmds.polyClean(mesh)

    # _freezeTransform transformations
    if storage.values.freezeTransform:
        if storage.values.displayInfo:
            ui.info("Info", "The script is freezing the transformations of your meshes")

        for node in storage.transformNodes:
            cmds.makeIdentity(node, apply=True, t=1, r=1, s=1, n=0)

    # delete history
    if storage.values.deleteHistory:
        if storage.values.displayInfo:
            ui.info("Info", "The script is deleting the history of your transformNodes")

        for node in storage.transformNodes:
            cmds.delete(node, constructionHistory=True)

    # export meshes
    if storage.values.exportResult:
        # Check or create a destination directory
        prepareExport(storage.sceneName, storage.values.exportName)

    # check non manyfold mesh
    probMesh = []
    cmds.select(clear=True)
    if storage.values.checkNonManyfold:
        if storage.values.displayInfo:
            ui.info("Info", "The script is looking for non-manyfold transformNodes")

        probMesh = checkNonManyfold()

    # set back the user to the original scene
    if storage.values.stayInScene:
        if storage.values.displayInfo:
            ui.info("Info", "You choose to stay in your active scene")

        cmds.file(save=True)
        cmds.file(storage.scene, open=True)

    if len(probMesh) > 0:
        for prob in probMesh:
            cmds.select(prob, add=True)

        ui.info("Non-manyfold transformNodes", "Problematic transformNodes have been seleted")

    cmds.undoInfo(cn="mayaExporterReady", cck=True)

    if storage.values.displayInfo:
        ui.info("Info", "The script has now finished !")

    print('\nFin du script\n')
