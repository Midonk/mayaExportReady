# coding=utf-8
"""
main app core
"""
import maya.cmds as cmds

freezeTransform = True
deleteHistory = True
conformNormals = True
bakePivot = True
cleanUpMesh = True
checkNaming = True
checkNonManyfold = True
setToUnityScale = False
displayInfo = True
meshes = None

"""
MANAGE THE UI
"""
# Create a window with custom controlers
def createWindow(name, callback):
    print("Ceate window named '{}'".format(name))
    if cmds.window("sanitizer", exists=True):
        cmds.deleteUI("sanitizer")
    _win = cmds.window("sanitizer", title=name)

    cmds.columnLayout(adjustableColumn=True)

    cmds.checkBox("freezeTransform", l="freezeTransform", v=freezeTransform)
    cmds.checkBox("deleteHistory", l="deleteHistory", v=deleteHistory)
    cmds.checkBox("conformNormals", l="conformNormals", v=conformNormals)
    cmds.checkBox("bakePivot", l="bakePivot", v=bakePivot)
    cmds.checkBox("cleanUpMesh", l="cleanUpMesh", v=cleanUpMesh)
    cmds.checkBox("checkNaming", l="checkNaming", v=checkNaming)
    cmds.checkBox("checkNonManyfold", l="checkNonManyfold", v=checkNonManyfold)
    cmds.checkBox("displayInfo", l="displayInfo", v=displayInfo)
    cmds.checkBox("setToUnityScale", l="setToUnityScale", v=setToUnityScale)

    cmds.button(l="Go", c=callback)

    # Montre la window passée en argument
    cmds.showWindow(_win)

    return _win


"""
CREATE CONFIRM MODAL WITH YES/NO BUTTONS
"""
def confirm(title, message, callbackYes, callbackNo):
    res = cmds.confirmDialog(title=title,
                             message=message,
                             button=["Yes", "No"],
                             defaultButton='Yes',
                             cancelButton='No',
                             dismissString='No')

    if res == "Yes":
        print("YES")
        callbackYes()
        return True

    else:
        # display results
        print("NO")
        callbackNo()
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
Link params
"""
def getParams():
    print("Getting parameter")
    global freezeTransform
    global deleteHistory
    global conformNormals
    global bakePivot
    global cleanUpMesh
    global checkNaming
    global checkNonManyfold
    global setToUnityScale
    global displayInfo
    freezeTransform = cmds.checkBox("freezeTransform", q=True, v=True)
    deleteHistory = cmds.checkBox("deleteHistory", q=True, v=True)
    conformNormals = cmds.checkBox("conformNormals", q=True, v=True)
    bakePivot = cmds.checkBox("bakePivot", q=True, v=True)
    cleanUpMesh = cmds.checkBox("cleanUpMesh", q=True, v=True)
    checkNaming = cmds.checkBox("checkNaming", q=True, v=True)
    checkNonManyfold = cmds.checkBox("checkNonManyfold", q=True, v=True)
    setToUnityScale = cmds.checkBox("setToUnityScale", q=True, v=True)
    displayInfo = cmds.checkBox("displayInfo", q=True, v=True)

    sanitizer()


"""
app definition
"""
def sanitizer():
    cmds.undoInfo(cn="sanitizer", ock=True)
    print('\nLancement du script\n')

    # Aware the user of what it will happen
    if displayInfo:
        info("Info", "Your scene will be duplicated, blablabla, ...")

# Wright metadata
# Check if there is no duplicated project

# Duplicate the project

# Opening of the new project into Maya

# Getting all meshes

    global meshes
    meshes = cmds.ls(sl=True)



    if len(meshes) == 0:
        info("Error", "No mesh selected")
        print('\nFin du script\n')
        return

    print(meshes)

    # check freeze transform
    if freezeTransform:
        problematicMeshes = []
        for mesh in meshes:
            pos = cmds.xform(mesh, q=True, t=True)
            rot = cmds.xform(mesh, q=True, ro=True)
            scale = cmds.xform(mesh, q=True, s=True, r=True)

            # the mesh is conform
            if pos == [0.0, 0.0, 0.0] and rot == [0.0, 0.0, 0.0] and scale == [1.0, 1.0, 1.0]:
                pass
                # print("FreezeTransform is OK")

            # the mesh isn't conform
            else:
                # print("FreezeTransform ERROR")
                print("=> store " + mesh)
                problematicMeshes.append(mesh)

        # problematic meshes found
        if len(problematicMeshes) > 0:
            # Freeze transform
            def callbackYes():
                for problematicMesh in problematicMeshes:
                    cmds.makeIdentity(problematicMesh, apply=True, t=1, r=1, s=1, n=0)

            def callbackNo():
                cmds.select(clear=True)
                for problematicMesh in problematicMeshes:
                    cmds.select(problematicMesh, add=True)

                if displayInfo:
                    info("Freeze transform", "Problematic meshes have been selected")

            goFurther = confirm("Freeze transform",
                                "One or several meshes don't have frozen transformations. Do you want to freeze them automaticaly ?",
                                callbackYes, callbackNo)

            if not goFurther:
                print('\nFin du script\n')
                return

    # check delete history
    if deleteHistory:
        for mesh in meshes:
            print(cmds.listHistory(mesh, q=True, ha=True))

    # check normals
    if conformNormals:
        for mesh in meshes:
            # set all normal to conform mode
            cmds.select(mesh + '.f[*]')
            meshFaces = cmds.filterExpand(cmds.ls(sl=True), sm=34)
            cmds.select(mesh)
            for face in meshFaces:
                print(face)
                print(cmds.polyNormal(face, q=True, nm=True))

    # set pivot of the mesh on maya pivot

    # clean up

    # nomenclature correcte

    # check non manyfold mesh

    cmds.undoInfo(cn="sanitizer", cck=True)


# Launch app
win = createWindow("Sanitizer", "getParams()")
