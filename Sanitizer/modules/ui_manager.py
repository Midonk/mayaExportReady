# coding=utf-8

import maya.cmds as cmds
import os
import params
from Sanitizer import storage
import utility


def getRebuildOption():
    return cmds.radioButtonGrp("rebuildNormalOption", q=True, select=True) == 3


def enableCustomAngle(value):
    if value:
        cmds.intField("customNormalAngle", e=True, enable=getRebuildOption())
    else:
        cmds.intField("customNormalAngle", e=True, enable=False)


def enableRebuildOption(value):
    cmds.radioButtonGrp("rebuildNormalOption", e=True, enable=value)
    enableCustomAngle(value)


def onEnableExport(value):
    cmds.button("exportFolderBrowserButton", e=True, enable=value)
    cmds.textField("exportFolderInput", e=True, enable=value)
    cmds.textField("exportNameInput", e=True, enable=value)
    cmds.text("radioColExtentionLabel", e=True, enable=value)
    cmds.radioButton("exportFbx", e=True, enable=value)
    cmds.radioButton("exportObj", e=True, enable=value)


# Open file dialog to choose the reference directory
def searchRefs(*args):
    directory = cmds.fileDialog2(ds=2, fm=3, dir=storage.unityRefDir)
    if directory is not None:
        directory = directory[0]
        storage.unityRefDir = directory
        displayRefs(directory)
        utility.setUnityRefDir()
        return

    info("Search reference", "No folder selected")


# Open file dialog to choose the export folder
def searchExportFolder(*args):
    directory = cmds.fileDialog2(ds=2, fm=2, dir=storage.values.exportFolder)
    if directory is not None:
        directory = directory[0]
        storage.values.exportFolder = directory
        utility.setExportFolder()
        cmds.textField("exportFolderInput", e=True, text=directory)
        return

    info("Search export folder", "No folder selected")


# Searches 'obj' or 'fbx' references into the specified folder and displays it into the 'Sanitizer' window
def displayRefs(refDir):
    if cmds.columnLayout("refContainer", q=True, exists=True):
        cmds.deleteUI("refContainer", layout=True)

    storage.unityRefs.clear()
    cmds.columnLayout("refContainer", p="refWraper")
    cmds.radioCollection("unityRefs")
    refFbx = cmds.getFileList(folder=refDir, filespec="*.fbx") or []
    refObj = cmds.getFileList(folder=refDir, filespec="*.obj") or []
    cmds.button('unityImportRef', e=True, enable=len(refFbx) > 0 or len(refObj))

    if len(refFbx) > 0:
        cmds.text(l="")
        cmds.text(l="FBX:")

    for ref in refFbx:
        refName, refExt = os.path.splitext(ref)
        storage.unityRefs[refName] = refExt
        cmds.radioButton(refName, l=refName)

    if len(refObj) > 0:
        cmds.text(l="")
        cmds.text(l="OBJ:")

    for ref in refObj:
        refName, refExt = os.path.splitext(ref)
        storage.unityRefs[refName] = refExt
        cmds.radioButton(os.path.basename(ref), l=os.path.splitext(ref)[0])

    cmds.text(l="")
    cmds.setParent('..')
    cmds.setParent('..')


# Import in open scene the selected reference
def importRef(*args):
    ref = cmds.radioCollection("unityRefs", q=True, select=True)
    if ref != "NONE":
        path = os.path.join(storage.unityRefDir, ref + storage.unityRefs[ref])
        importedNodes = cmds.file(path, i=True, mergeNamespacesOnClash=True, returnNewNodes=True)
        cmds.select(clear=True)
        for node in importedNodes:
            cmds.select(node, add=True)

    else:
        info("Import error", "You have to select an element to import")


# Check if the folder specified to the export folder, exists
def checkExportFolder(path):
    # Register the new export folder
    if cmds.file(path, q=True, exists=True):
        storage.values.exportFolder = path
        utility.setExportFolder()
        cmds.textField("exportFolderInput", e=True, text=path)

    # Reset the export folder by the saved one
    else:
        cmds.textField("exportFolderInput", e=True, text=storage.values.exportFolder)


def onFbxExtension(value):
    storage.values.exportExtension = "exportFbx"
    utility.setExportExtension()


def onObjExtension(value):
    storage.values.exportExtension = "exportObj"
    utility.setExportExtension()

def updateExportName(name):
    storage.values.exportName = name
    utility.setExportName()


# Create the UI for the sanitizer
def createWindow(name, callback):
    print('\nLancement du script\n')

    # check if the window exists already
    if cmds.window("sanitizer", exists=True):
        cmds.deleteUI("sanitizer")
    _win = cmds.window("sanitizer", title=name)

    cmds.rowColumnLayout("global", adjustableColumn=True, columnOffset=[1, "both", storage.globalColumnOffset])
    cmds.shelfTabLayout('mainShelfTab', w=storage.shelfWidth)

    # GENERAL PANEL
    cmds.columnLayout("General", adj=False, columnOffset=["both", storage.inShelfOffset])
    cmds.text(l='<span style="font-size:18px">Manage general options</span>', font="boldLabelFont")
    cmds.text(l="")
    cmds.checkBox("freezeTransform", l="Freeze transformations", v=storage.values.freezeTransform)
    cmds.checkBox("deleteHistory", l="Delete history", v=storage.values.deleteHistory)
    cmds.checkBox("selectionOnly", l="Selection only", v=storage.values.selectionOnly)
    cmds.checkBox("cleanUpMesh", l="Clean up meshes", v=storage.values.cleanUpMesh)
    cmds.checkBox("checkNonManyfold", l="Check for non-manyfold meshes", v=storage.values.checkNonManyfold)
    cmds.text(l="")
    cmds.setParent('..')

    # NORMAL PANEL
    cmds.columnLayout("Normal", adj=False, columnOffset=["both", storage.inShelfOffset])
    cmds.text(l='<span style="font-size:18px">Manage normals options</span>', font="boldLabelFont")
    cmds.text(l="")
    cmds.checkBox("conformNormals", l="Conform normals", v=storage.values.conformNormals)
    cmds.checkBox("rebuildNormals", l="Rebuild normals", v=storage.values.rebuildNormals, cc=enableRebuildOption)
    cmds.text(label="")
    cmds.text(label="Rebuild options:", align="left")
    cmds.radioButtonGrp("rebuildNormalOption", labelArray3=['Soft', 'Hard', 'Custom'],
                        numberOfRadioButtons=3,
                        select=storage.values.rebuildNormalOption,
                        vertical=True,
                        enable=storage.values.rebuildNormals,
                        cc=enableCustomAngle)
    cmds.intField("customNormalAngle", min=0, max=180, v=storage.values.customNormalAngle, enable=getRebuildOption())
    cmds.text(l="")
    cmds.setParent('..')

    # PIVOT PANEL
    cmds.columnLayout("Pivot", adj=False, columnOffset=["both", storage.inShelfOffset])
    cmds.text(l='<span style="font-size:18px">Manage pivot options</span>', font="boldLabelFont")
    cmds.text(l="")
    cmds.text(label="Options:", align="left")
    cmds.radioButtonGrp("pivotOption",
                        labelArray4=['Untouched', 'Mesh center', 'Scene center', 'Base center'],
                        numberOfRadioButtons=4,
                        select=storage.values.pivotOption,
                        vertical=True)
    cmds.text(l="")
    cmds.setParent('..')

    # EXPORT PANEL
    cmds.columnLayout("Export", adj=False, columnOffset=["both", storage.inShelfOffset])
    cmds.text(l='<span style="font-size:18px">Export settings</span>', font="boldLabelFont")
    cmds.text(l="")
    cmds.checkBox("exportResult", l="Export result", v=storage.values.exportResult, cc=onEnableExport)
    cmds.rowLayout(adjustableColumn=2, numberOfColumns=2)
    cmds.textField("exportFolderInput", fi=storage.values.exportFolder, w=300, h=26, cc=checkExportFolder)
    cmds.button("exportFolderBrowserButton", l="Browse", c=searchExportFolder)
    cmds.setParent('..')
    cmds.text(l="")
    cmds.text(l="Mesh name")
    cmds.textField("exportNameInput", text=storage.values.exportName, w=351, h=26, cc=updateExportName)
    cmds.radioCollection("exportExtension")
    cmds.text(l="")
    cmds.text("radioColExtentionLabel", l="Export as")
    cmds.radioButton("exportFbx", l="FBX", onCommand=onFbxExtension)
    cmds.radioButton("exportObj", l="OBJ", onCommand=onObjExtension)
    cmds.radioCollection("exportExtension", e=True, select=storage.values.exportExtension)

    onEnableExport(cmds.checkBox("exportResult", q=True, v=True))
    cmds.text(l="")
    cmds.setParent('..')


    # REFERENCE PANEL
    cmds.columnLayout("References", adj=False, columnOffset=["both", storage.inShelfOffset])
    cmds.text(l='<span style="font-size:18px">Search and import references</span>', font="boldLabelFont")
    cmds.columnLayout("refWraper")
    cmds.setParent('..')
    cmds.rowLayout(adjustableColumn=2, numberOfColumns=2)
    cmds.button(label="Search", c=searchRefs, w=150)
    cmds.button('unityImportRef', l='Import reference', c=importRef, w=150)
    cmds.setParent('..')
    cmds.text(l="")
    displayRefs(storage.unityRefDir)
    cmds.setParent('..')

    # SETTINGS PANEL
    cmds.columnLayout("Settings", adj=False, columnOffset=["both", storage.inShelfOffset])
    cmds.text(l='<span style="font-size:18px">Manage the settings</span>', font="boldLabelFont")
    cmds.text(l="")
    cmds.checkBox("alwaysOverrideExport", l="Override existing export file", v=storage.values.alwaysOverrideExport)
    cmds.checkBox("displayInfo", l="Display informations", v=storage.values.displayInfo)
    cmds.text(l="")

    cmds.setParent('|')
    cmds.text(l="")
    cmds.button(l="Go", c=callback)
    cmds.rowColumnLayout("global", e=True, rowOffset=[(1, "top", storage.globalRowOffset), (
        len(cmds.rowColumnLayout("global", q=True, childArray=True)), "bottom", storage.globalRowOffset)])

    # Display the window
    cmds.showWindow(_win)

    return _win


"""
CREATE MODAL
"""


# Create confirm modal with 'Yes' / 'No' buttons
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


# Create info modal with just an 'ok' button
def info(title, message):
    cmds.confirmDialog(title=title,
                       message=message,
                       button=["Ok"],
                       defaultButton='Ok',
                       dismissString='Ok')
