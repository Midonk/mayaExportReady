import maya.cmds as cmds
import os
import ui_manager as ui
import utility
from Sanitizer import storage

fileExists = cmds.file(storage.scene, q=True, exists=True)
fileModified = cmds.file(storage.scene, q=True, modified=True)


# Manage the save process following the scene state
def saveScene():
    if not fileExists:
        # The file has already a name
        if storage.scene != "":
            cmds.file(save=True)

        # the file need a name => then a location
        else:
            scene = cmds.fileDialog2(ds=2, fm=0)
            if scene is not None:
                storage.scene = scene[0]
                sceneName = os.path.splitext(storage.scene)[0]
                storage.scene = cmds.file(scene, rename=sceneName + '.ma')
                cmds.file(save=True, type='mayaAscii')
                print("scene saved as", storage.scene)

            # The user canceled the dialog
            else:
                if storage.values.displayInfo:
                    ui.info("Warning", "The script can't continue without saving")
                print("\nEnd of script\n")

    elif fileModified:
        cmds.file(save=True)

    global fileExists
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
    if "_export" in sceneName:
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


# Split transform nodes between meshes and groups
def splitTransform():
    storage.transformNodes = cmds.ls(sl=True, type="transform")
    for node in storage.transformNodes:
        if utility.isGroup(node):
            storage.groups.append(node)

        else:
            storage.meshes.append(node)

    print("transformNodes", storage.transformNodes)
    print("meshes", storage.meshes)
    print("groups", storage.groups)


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
        print("nme", nme)
        print("nmv", nmv)
        print("nue", nue)
        print("nuv", nuv)

        if nme is not None or nue is not None or nuv is not None or nmv is not None:
            probMesh.append(mesh)

    if len(probMesh) > 0:
        for prob in probMesh:
            cmds.select(prob, add=True)

        ui.info("Non-manyfold transformNodes", "Problematic transformNodes have been seleted")


"""
app definition
"""


def sanitizer():
    cmds.undoInfo(cn="sanitizer", ock=True)
    # Aware the user of what it will happen
    if storage.values.displayInfo:
        ui.info("Info",
                "The script will nowproceed through several operations, as you parametered it in the preceding window")

    # """""""""""""

    #  CHECK FILES

    # """""""""""""

    # check the localization of the file
    storage.scene = cmds.file(q=True, sn=True)

    if not checkSave():
        return

    sceneName, sceneExtension = os.path.splitext(os.path.basename(storage.scene))

    # check if the file is not an export file
    if not checkExportFile(sceneName):
        return

    # Check if there is no duplicated project
    sceneCopy = os.path.join(os.path.dirname(storage.scene), sceneName + "_export" + sceneExtension)

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

    cmds.file(sceneCopy, open=True)

    # """""""""""""""""""""

    #  PREPARE THE PROCESS

    # """""""""""""""""""""

    # Getting all transformNodes needed
    if storage.values.displayInfo:
        ui.info("Info", "The script gather all the transformNodes of the scene to prepare them to the export")

    if not storage.values.selectionOnly:
        cmds.select(all=True, hierarchy=True)

    # Splitting into meshes and groups
    splitTransform()

    # Make sure that at least one mesh or group is selected
    if len(storage.transformNodes) == 0:
        ui.info("Error", "No mesh or group detected in your scene")
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

    cmds.select(clear=True)

    # check non manyfold mesh
    if storage.values.checkNonManyfold:
        if storage.values.displayInfo:
            ui.info("Info", "The script is looking for non-manyfold transformNodes")

        checkNonManyfold()

        # freeze transformations
        if storage.values.freezeTransform:
            if storage.values.displayInfo:
                ui.info("Info", "The script is freezing the transformations of yourmeshes")

            for node in storage.transformNodes:
                cmds.makeIdentity(node, apply=True, t=1, r=1, s=1, n=0)

        # delete history
        if storage.values.deleteHistory:
            if storage.values.displayInfo:
                ui.info("Info", "The script is deleting the history of your transformNodes")

            for node in storage.transformNodes:
                cmds.delete(node, constructionHistory=True)

    cmds.undoInfo(cn="sanitizer", cck=True)

    if storage.values.displayInfo:
        ui.info("Info", "The script has now finished !")
