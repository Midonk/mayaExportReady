import maya.cmds as cmds
import process
from Sanitizer import storage
import utility

"""
Link params between UI and script
"""


def getParams():
    storage.values.freezeTransform = cmds.checkBox("freezeTransform", q=True, v=True)
    storage.values.deleteHistory = cmds.checkBox("deleteHistory", q=True, v=True)
    storage.values.selectionOnly = cmds.checkBox("selectionOnly", q=True, v=True)
    storage.values.conformNormals = cmds.checkBox("conformNormals", q=True, v=True)
    storage.values.rebuildNormals = cmds.checkBox("rebuildNormals", q=True, v=True)
    storage.values.rebuildNormalOption = cmds.radioButtonGrp("rebuildNormalOption", q=True, select=True)
    storage.values.customNormalAngle = cmds.intField("customNormalAngle", q=True, v=True)
    storage.values.pivotOption = cmds.radioButtonGrp("pivotOption", q=True, select=True)
    storage.values.cleanUpMesh = cmds.checkBox("cleanUpMesh", q=True, v=True)
    storage.values.checkNonManyfold = cmds.checkBox("checkNonManyfold", q=True, v=True)
    storage.values.alwaysOverrideExport = cmds.checkBox("alwaysOverrideExport", q=True, v=True)
    storage.values.displayInfo = cmds.checkBox("displayInfo", q=True, v=True)

    utility.setAllMetadata()

    cmds.deleteUI("sanitizer")
    process.sanitizer()
