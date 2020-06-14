import maya.cmds as cmds
import os
import ui_manager as ui
import utility

scene = None
fileExists = cmds.file(scene, q=True, exists=True)
fileModified = cmds.file(scene, q=True, modified=True)


"""
app definition
"""


def sanitizer(values):
    # Manage the save process following the scene state
    def saveScene():
        global scene
        if not fileExists:
            # The file has already a name
            if scene != "":
                cmds.file(scene, save=True)

            else:
                scene = cmds.fileDialog2(ds=2, fm=0)
                # The user canceled the dialog
                if scene is not None:
                    scene = scene[0]
                    sName = os.path.splitext(scene)[0]
                    scene = cmds.file(scene, rename=sName + '.ma')
                    cmds.file(scene, save=True, type='mayaAscii')
                    print("scene saved as", scene)

                else:
                    if values.displayInfo:
                        ui.info("Warning", "The script can't continue without saving")
                    print("\nEnd of script\n")

        elif fileModified:
            cmds.file(scene, save=True)

    def checkSave():
        global scene
        # check if the scene exists in the os or if it has been modified

        if not fileExists or fileModified:
            if ui.confirm("Save scene",
                          "You need to save your scene before using this script\n\nDo you want to save your scene now ?\n"):

                saveScene()
                return True

            else:
                print("\nEnd of script\n")
                return False

        return True

    def checkExportFile():
        if fileExists:
            if "_export" in sceneName:
                if not ui.confirm("File duplication",
                                  "It seems the open scene is already an export file.\n"
                                  "\nAre you sure you want to run the script on this scene ?\n"):
                    print("\nEnd of script\n")
                    return False

        return True

    def checkDuplication(file):
        if fileExists:
            if values.displayInfo:
                ui.info("Info", "The script is now checking for an existing export file generated earlier")

            if not values.alwaysOverrideExport and cmds.file(file, q=True, exists=True):
                if not ui.confirm("Override export file",
                                  "An export file of this scene may already exist.\n\nDo you want to override it ?"):
                    print("\nEnd of script\n")
                    return False

        return True

    cmds.undoInfo(cn="sanitizer", ock=True)
    # Aware the user of what it will happen
    if values.displayInfo:
        ui.info("Info",
            "The script will nowproceed through several operations, as you parametered it in the preceding window")

    # """""""""""""

    #  CHECK FILES

    # """""""""""""

    #  CHECK SAVE
    # """"""""""""

    # check the localization of the file
    global scene
    scene = cmds.file(q=True, sn=True)

    if not checkSave(scene):
        return

    sceneName, sceneExtension = os.path.splitext(os.path.basename(scene))

    #  CHECK EXPORT FILE
    # """""""""""""""""""

    # check if the file is not an export file
    if not checkExportFile():
        return

    # Wright metadata

    #  SCENE DUPLICATION
    # """""""""""""""""""

    # Check if there is no duplicated project
    sceneCopy = os.path.join(os.path.dirname(scene), sceneName + "_export" + sceneExtension)

    if not checkDuplication(sceneCopy):
        return

    # Duplicate the project
    if values.displayInfo:
        ui.info("Info", "The script duplicate your scene as an 'export' file")

    cmds.sysFile(scene, copy=sceneCopy)

    # Opening of the new project into Maya
    if values.displayInfo:
        ui.info("Info", "The script is opening the duplicated scene in Maya")

    cmds.file(sceneCopy, open=True)
    print("sceneCopy", sceneCopy)

    # """""""""""""""""""""

    #  PREPARE THE PROCESS

    # """""""""""""""""""""

    # Getting all transformNodes in the scene
    if values.displayInfo:
        ui.info("Info", "The script gather all the transformNodes of the scene to prepare them to the export")

    cmds.select(all=True, hierarchy=True)

    # Splittinginto meshes and groups
    transformNodes = cmds.ls(sl=True, type="transform")
    meshes = []
    groups = []
    for mesh in transformNodes:
        if utility.isGroup(mesh):
            groups.append(mesh)

        else:
            meshes.append(mesh)

    print("meshes", meshes)
    print("groups", groups)

    # Make sure at list one mesh or group is selected
    if len(transformNodes) == 0:
        ui.info("Error", "No mesh or group detected in your scene")
        print('\nFin du script\n')
        return

    print("transformNodes", transformNodes)

    if values.displayInfo:
        ui.info("Info", "The script is ready to prepare your transformNodes")

    # """""""""

    #  PROCESS

    # """""""""

    # conform normals
    if values.conformNormals:
        if values.displayInfo:
            ui.info("Info", "The script conform the normals of your transformNodes as you asked for")

        for mesh in meshes:
            cmds.polyNormal(mesh, nm=2)

    # Rebuild normals
    if values.rebuildNormals:
        if values.displayInfo:
            ui.info("Info",
                "The script rebuild the normals of your transformNodes as you asked for, with parameter " + str(
                    values.rebuildNormalOption))

        for mesh in meshes:
            if values.rebuildNormalOption == 1:
                cmds.polySoftEdge(mesh, a=30)

            elif values.rebuildNormalOption == 2:
                cmds.polySoftEdge(mesh, a=0)

            elif values.rebuildNormalOption == 3:
                cmds.polySoftEdge(mesh, a=values.customNormalAngle)

    # set pivot of the
    if values.pivotOption == 2:
        if values.displayInfo:
            ui.info("Info", "The script set the pivot of your mesh at the center of them")
        for mesh in meshes:
            cmds.xform(mesh, r=True, centerPivots=True)

    elif values.pivotOption == 3:
        if values.displayInfo:
            ui.info("Info", "The script set the pivot of your mesh at the center of scene")
        for mesh in meshes:
            cmds.xform(mesh, ws=True, pivots=[0, 0, 0])
        print("opt center scene")

    elif values.pivotOption == 4:
        if values.displayInfo:
            ui.info("Info", "The script set the pivot of your mesh at the center of the bottom of your mesh")
        for mesh in meshes:
            cmds.xform(mesh, r=True, centerPivots=True)
            pivotPos = cmds.xform(mesh, q=True, pivots=True, ws=True)
            print("pivotPos", pivotPos)

            # Get vtx pos from  Narann => https://www.fevrierdorian.com/blog/post/2011/09/27/Quickly-retrieve-vertex-positions-of-a-Maya-mesh-%28English-Translation%29
            vtxWorldPosition = []
            vtxIndexList = cmds.getAttr(mesh + ".vrts", multiIndices=True)
            for i in vtxIndexList:
                curPointPosition = cmds.xform(mesh + ".pnts[" + str(i) + "]", q=True, t=True, ws=True)
                vtxWorldPosition.append(curPointPosition)
            # end of Narann code

            def sortinFct(e):
                return e[1]

            vtxWorldPosition.sort(key=sortinFct)
            cmds.xform(mesh, ws=True, pivots=[pivotPos[0], vtxWorldPosition[0][1], pivotPos[2]])

    # clean up
    if values.cleanUpMesh:
        if values.displayInfo:
            ui.info("Info", "The script is cleaning your mesh")

        for mesh in meshes:
            cmds.polyClean(mesh)

    cmds.select(clear=True)

    # check non manyfold mesh
    if values.checkNonManyfold:
        if values.displayInfo:
            ui.info("Info", "The script is looking for non-manyfold transformNodes")

        probMesh = []
        for mesh in meshes:
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
                cmds.select(clear=True)
                cmds.select(prob, add=True)

            ui.info("Non-manyfold transformNodes", "Problematic transformNodes have been seleted")

        # freeze transformations
        if values.freezeTransform:
            if values.displayInfo:
                ui.info("Info", "The script is freezing the transformations of yourmeshes")

            for node in transformNodes:
                cmds.makeIdentity(node, apply=True, t=1, r=1, s=1, n=0)

        # delete history
        if values.deleteHistory:
            if values.displayInfo:
                ui.info("Info", "The script is deleting the history of your transformNodes")

            for node in transformNodes:
                cmds.delete(node, constructionHistory=True)

    cmds.undoInfo(cn="sanitizer", cck=True)

    if values.displayInfo:
        ui.info("Info", "The script has now finished !")
