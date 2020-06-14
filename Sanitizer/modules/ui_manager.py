import maya.cmds as cmds
import os
import params

"""
MANAGE THE UI
"""


refs = []
def createWindow(name, callback, defaultValues):
    print('\nLancement du script\n')

    # check if the window exists already
    if cmds.window("sanitizer", exists=True):
        cmds.deleteUI("sanitizer")
    _win = cmds.window("sanitizer", title=name)

    # GENERAL PANEL
    cmds.columnLayout("global", adjustableColumn=True)
    cmds.shelfTabLayout('mainShelfTab')
    cmds.columnLayout("General", adj=True)
    cmds.checkBox("freezeTransform", l="Freeze transformations", v=defaultValues.freezeTransform)
    cmds.checkBox("deleteHistory", l="Delete history", v=defaultValues.deleteHistory)
    cmds.checkBox("cleanUpMesh", l="Clean up meshes", v=defaultValues.cleanUpMesh)
    cmds.checkBox("checkNonManyfold", l="Check for non-manyfold meshes", v=defaultValues.checkNonManyfold)
    cmds.setParent('..')

    # NORMAL PANEL
    cmds.columnLayout("Normal", adj=True)
    cmds.checkBox("conformNormals", l="Conform normals", v=defaultValues.conformNormals)
    cmds.checkBox("rebuildNormals", l="Rebuild normals", v=defaultValues.rebuildNormals,
                  cc=lambda onChange:
                  cmds.radioButtonGrp("rebuildNormalOption", e=True,
                                      enable=cmds.checkBox("rebuildNormals", q=True, v=True)))
    cmds.text(label="Rebuild options:", align="left")
    cmds.radioButtonGrp("rebuildNormalOption", labelArray3=['Soft', 'Hard', 'Custom'], numberOfRadioButtons=3,
                        select=defaultValues.rebuildNormalOption,
                        vertical=True,
                        enable=defaultValues.rebuildNormals,
                        cc=lambda onChange:
                        cmds.intField("customNormalAngle", e=True,
                                      enable=cmds.radioButtonGrp("rebuildNormalOption", q=True,
                                                                 select=True) == 3))
    cmds.intField("customNormalAngle", min=0, max=180, v=defaultValues.customNormalAngle,
                  enable=(cmds.radioButtonGrp("rebuildNormalOption", q=True, select=True) == 3))
    cmds.setParent('..')

    # PIVOT PANEL
    cmds.columnLayout("Pivot", adj=True)
    cmds.text(label="Options:", align="left")
    cmds.radioButtonGrp("pivotOption", labelArray4=['Untouched', 'Mesh center', 'Scene center', 'Base center'],
                        numberOfRadioButtons=4,
                        select=defaultValues.pivotOption,
                        vertical=True)
    cmds.setParent('..')

    # UITY PANEL
    cmds.columnLayout("Unity", adj=True)

    def searchRefs(*args):
        global refs
        refs = cmds.fileDialog2(ds=2, fm=4,
                                     ff='Any (*.*);;Maya ASCII (*.ma);;Maya binary (*.mb);;FBX (*.fbx);; OBJ (*.obj)')

    cmds.button(label="Search", c=searchRefs)
    for ref in refs:
        cmds.button(l=os.path.splitext(ref)[0])

    cmds.setParent('..')

    # SETTINGS PANEL
    cmds.columnLayout("Settings", adj=True)
    cmds.checkBox("alwaysOverrideExport", l="Override existing export file", v=defaultValues.alwaysOverrideExport)
    cmds.checkBox("displayInfo", l="Display informations", v=defaultValues.displayInfo)

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
