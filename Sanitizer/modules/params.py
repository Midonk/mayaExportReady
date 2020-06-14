import maya.cmds as cmds
import process as process

"""
Link params between UI and script
"""


def getParams(values):
    values.freezeTransform = cmds.checkBox("freezeTransform", q=True, v=True)
    values.deleteHistory = cmds.checkBox("deleteHistory", q=True, v=True)
    values.conformNormals = cmds.checkBox("conformNormals", q=True, v=True)
    values.rebuildNormals = cmds.checkBox("rebuildNormals", q=True, v=True)
    values.rebuildNormalOption = cmds.radioButtonGrp("rebuildNormalOption", q=True, select=True)
    values.customNormalAngle = cmds.intField("customNormalAngle", q=True, v=True)
    values.pivotOption = cmds.radioButtonGrp("pivotOption", q=True, select=True)
    values.cleanUpMesh = cmds.checkBox("cleanUpMesh", q=True, v=True)
    values.checkNonManyfold = cmds.checkBox("checkNonManyfold", q=True, v=True)
    values.alwaysOverrideExport = cmds.checkBox("alwaysOverrideExport", q=True, v=True)
    values.displayInfo = cmds.checkBox("displayInfo", q=True, v=True)

    process.sanitizer(values)
