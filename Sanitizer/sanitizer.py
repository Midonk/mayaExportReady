# coding=utf-8
"""
main app core
"""
import maya.cmds as cmds
import os

freezeTransform = True
deleteHistory = True
conformNormals = True
rebuildNormals = True
rebuildNormalOption = 0
customNormalAngle = 60
bakePivot = True
pivotOption = 1
cleanUpMesh = True
checkNonManyfold = True
unityRefs = []
alwaysOverrideExport = False
displayInfo = True

"""
MANAGE THE UI
"""


def createWindow(name, callback):
    print('\nLancement du script\n')

    # check if the window exists already
    if cmds.window("sanitizer", exists=True):
        cmds.deleteUI("sanitizer")
    _win = cmds.window("sanitizer", title=name)

    # GENERAL PANEL
    cmds.columnLayout("global", adjustableColumn=True)
    cmds.shelfTabLayout('mainShelfTab')
    cmds.columnLayout("General", adj=True)
    cmds.checkBox("freezeTransform", l="Freeze transformations", v=freezeTransform)
    cmds.checkBox("deleteHistory", l="Delete history", v=deleteHistory)
    cmds.checkBox("cleanUpMesh", l="Clean up meshes", v=cleanUpMesh)
    cmds.checkBox("checkNonManyfold", l="Check for non-manyfold meshes", v=checkNonManyfold)
    cmds.setParent('..')

    # NORMAL PANEL
    cmds.columnLayout("Normal", adj=True)
    cmds.checkBox("conformNormals", l="Conform normals", v=conformNormals)
    cmds.checkBox("rebuildNormals", l="Rebuild normals", v=rebuildNormals,
                  cc=lambda onChange:
                  cmds.radioButtonGrp("rebuildNormalOption", e=True,
                                      enable=cmds.checkBox("rebuildNormals", q=True, v=True)))
    cmds.text(label="Rebuild options:", align="left")
    cmds.radioButtonGrp("rebuildNormalOption", labelArray3=['Soft', 'Hard', 'Custom'], numberOfRadioButtons=3,
                        select=rebuildNormalOption,
                        vertical=True,
                        enable=rebuildNormals,
                        cc=lambda onChange:
                        cmds.intField("customNormalAngle", e=True,
                                      enable=cmds.radioButtonGrp("rebuildNormalOption", q=True,
                                                                 select=True) == 3))
    cmds.intField("customNormalAngle", min=0, max=180, v=customNormalAngle,
                  enable=(cmds.radioButtonGrp("rebuildNormalOption", q=True, select=True) == 3))
    cmds.setParent('..')

    # PIVOT PANEL
    cmds.columnLayout("Pivot", adj=True)
    cmds.text(label="Options:", align="left")
    cmds.radioButtonGrp("pivotOption", labelArray4=['Untouched', 'Mesh center', 'Scene center', 'Base center'], numberOfRadioButtons=4,
                        select=pivotOption,
                        vertical=True)
    cmds.setParent('..')

    # UITY PANEL
    cmds.columnLayout("Unity", adj=True)

    def searchRefs(*args):
        global unityRefs
        unityRefs = cmds.fileDialog2(ds=2, fm=4,
                                     ff='Any (*.*);;Maya ASCII (*.ma);;Maya binary (*.mb);;FBX (*.fbx);; OBJ (*.obj)')

    cmds.button(label="Search", c=searchRefs)
    global unityRefs
    for ref in unityRefs:
        cmds.button(l=os.path.splitext(ref)[0])

    cmds.setParent('..')

    # SETTINGS PANEL
    cmds.columnLayout("Settings", adj=True)
    cmds.checkBox("alwaysOverrideExport", l="Override existing export file", v=alwaysOverrideExport)
    cmds.checkBox("displayInfo", l="Display informations", v=displayInfo)

    cmds.setParent('|')
    cmds.button(l="Go", c=callback)

    # Display the window
    cmds.showWindow(_win)

    return _win


"""
CREATE CONFIRM MODAL WITH YES/NO BUTTONS
"""


def confirm(title, message):
    print("Display " + title + " confirm")
    res = cmds.confirmDialog(title=title,
                             message=message,
                             button=["Yes", "No"],
                             defaultButton='Yes',
                             cancelButton='No',
                             dismissString='No')

    if res == "Yes":
        print("Answer => YES")
        return True

    else:
        # display results
        print("Answer => NO")
        return False


"""
CREATE INFO MODAL
"""


def info(title, message):
    cmds.confirmDialog(title=title,
                       message=message,
                       button=["Ok"],
                       defaultButton='Ok',
                       dismissString='Ok')


"""
UTILITY INFO
"""


def utility(title, message):
    if displayInfo:
        info(title, message)

"""
GROUP FINDER
"""
def isGroup(element):
    children = cmds.listRelatives(element, children=True)
    for child in children:
        if not cmds.ls(child, transforms = True):
            return False
    return True

"""
Link params between UI and script
"""


def getParams():
    global freezeTransform
    global deleteHistory
    global conformNormals
    global rebuildNormals
    global rebuildNormalOption
    global customNormalAngle
    global pivotOption
    global cleanUpMesh
    global checkNonManyfold
    global alwaysOverrideExport
    global displayInfo
    freezeTransform = cmds.checkBox("freezeTransform", q=True, v=True)
    deleteHistory = cmds.checkBox("deleteHistory", q=True, v=True)
    conformNormals = cmds.checkBox("conformNormals", q=True, v=True)
    rebuildNormals = cmds.checkBox("rebuildNormals", q=True, v=True)
    rebuildNormalOption = cmds.radioButtonGrp("rebuildNormalOption", q=True, select=True)
    customNormalAngle = cmds.intField("customNormalAngle", q=True, v=True)
    pivotOption = cmds.radioButtonGrp("pivotOption", q=True, select=True)
    cleanUpMesh = cmds.checkBox("cleanUpMesh", q=True, v=True)
    checkNonManyfold = cmds.checkBox("checkNonManyfold", q=True, v=True)
    alwaysOverrideExport = cmds.checkBox("alwaysOverrideExport", q=True, v=True)
    displayInfo = cmds.checkBox("displayInfo", q=True, v=True)

    sanitizer()


"""
app definition
"""


def sanitizer():
    cmds.undoInfo(cn="sanitizer", ock=True)
    # Aware the user of what it will happen
    utility("Info",
            "The script will nowproceed through several operations, as you parametered it in the preceding window")

    # """""""""""""

    #  CHECK FILES

    # """""""""""""

    #  CHECK SAVE
    # """"""""""""

    # check the localization of the file
    scene = cmds.file(q=True, sn=True)

    # check if the scene exists in the os or if it has been modified
    fileExists = cmds.file(scene, q=True, exists=True)
    fileModified = cmds.file(q=True, modified=True)
    if not fileExists or fileModified:
        if confirm("Save scene",
                   "You need to save your scene before using this script\n\nDo you want to save your scene now ?\n"):

            if not fileExists:
                # The file has already a name
                if scene != "":
                    cmds.file(save=True)

                else:
                    scene = cmds.fileDialog2(ds=2, fm=0)
                    # The user canceled the dialog
                    if scene is not None:
                        scene = scene[0]
                        sName = os.path.splitext(scene)[0]
                        scene = cmds.file(rename=sName + '.ma')
                        cmds.file(save=True, type='mayaAscii')
                        print("scene saved as", scene)

                    else:
                        utility("Warning", "The script can't continue without saving")
                        print("\nEnd of script\n")

            elif fileModified:
                cmds.file(save=True)

        else:
            print("\nEnd of script\n")
            return

    sceneName, sceneExtension = os.path.splitext(os.path.basename(scene))

    #  CHECK EXPORT FILE
    # """""""""""""""""""

    # check if the file is not an export file
    if fileExists:
        if "_export" in sceneName:
            if not confirm("File duplication",
                           "It seems the open scene is already an export file.\n"
                           "\nAre you sure you want to run the script on this scene ?\n"):
                print("\nEnd of script\n")
                return

    # Wright metadata

    #  SCENE DUPLICATION
    # """""""""""""""""""

    # Check if there is no duplicated project
    sceneCopy = os.path.join(os.path.dirname(scene), sceneName + "_export" + sceneExtension)

    if fileExists:
        utility("Info", "The script is now checking for an existing export file generated earlier")
        if not alwaysOverrideExport and cmds.file(sceneCopy, q=True, exists=True):
            if not confirm("Override export file",
                           "An export file of this scene may already exist.\n\nDo you want to override it ?"):
                print("\nEnd of script\n")
                return

    # Duplicate the project
    utility("Info", "The script duplicate your scene as an 'export' file")

    cmds.sysFile(scene, copy=sceneCopy)

    # Opening of the new project into Maya
    utility("Info", "The script is opening the duplicated scene in Maya")

    cmds.file(sceneCopy, open=True)
    print("sceneCopy", sceneCopy)

    # """""""""""""""""""""

    #  PREPARE THE PROCESS

    # """""""""""""""""""""

    # Getting all transformNodes in the scene
    utility("Info", "The script gather all the transformNodes of the scene to prepare them to the export")

    cmds.select(all=True, hierarchy=True)

    # Splittinginto meshes and groups
    transformNodes = cmds.ls(sl=True, type="transform")
    meshes = []
    groups = []
    for mesh in transformNodes:
        if isGroup(mesh):
            groups.append(mesh)

        else:
            meshes.append(mesh)

    print("meshes", meshes)
    print("groups", groups)

    if len(transformNodes) == 0:
        info("Error", "No mesh or group detected in your scene")
        print('\nFin du script\n')
        return

    print("transformNodes", transformNodes)

    utility("Info", "The script is ready to prepare your transformNodes")

    # """""""""

    #  PROCESS

    # """""""""

    # conform normals
    if conformNormals:
        utility("Info", "The script conform the normals of your transformNodes as you asked for")

        for mesh in meshes:
            cmds.polyNormal(mesh, nm=2)

    # Rebuild normals
    if rebuildNormals:
        utility("Info",
                "The script rebuild the normals of your transformNodes as you asked for, with parameter " + str(
                    rebuildNormalOption))

        for mesh in meshes:
            if rebuildNormalOption == 1:
                cmds.polySoftEdge(mesh, a=30)

            elif rebuildNormalOption == 2:
                cmds.polySoftEdge(mesh, a=0)

            elif rebuildNormalOption == 3:
                cmds.polySoftEdge(mesh, a=customNormalAngle)

    # set pivot of the
    if pivotOption == 2:
        utility("Info", "The script set the pivot of your mesh at the center of them")
        for mesh in meshes:
            cmds.xform(mesh, relative=True, centerPivots=True)

    elif pivotOption == 3:
        utility("Info", "The script set the pivot of your mesh at the center of scene")
        for mesh in meshes:
            cmds.xform(mesh,worldSpace=True, pivots=[0, 0, 0])

    elif pivotOption == 4:
        utility("Info", "The script set the pivot of your mesh at the center of the bottom of your mesh")

        print("opt center scene")

    # clean up
    if cleanUpMesh:
        utility("Info", "The script is cleaning your mesh")

        for mesh in meshes:
            cmds.polyClean(mesh)

    cmds.select(clear=True)

    # check non manyfold mesh
    if checkNonManyfold:
        utility("Info", "The script is looking for non-manyfold transformNodes")

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

            info("Non-manyfold transformNodes", "Problematic transformNodes have been seleted")

        # freeze transformations
        if freezeTransform:
            utility("Info", "The script is freezing the transformations of yourmeshes")

            for node in transformNodes:
                cmds.makeIdentity(node, apply=True, t=1, r=1, s=1, n=0)

        # delete history
        if deleteHistory:
            utility("Info", "The script is deleting the history of your transformNodes")

            for node in transformNodes:
                cmds.delete(node, constructionHistory=True)

    cmds.undoInfo(cn="sanitizer", cck=True)

    utility("Info", "The script has now finished !")


# Launch app
win = createWindow("Sanitizer", "getParams()")
