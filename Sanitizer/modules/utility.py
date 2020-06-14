import maya.cmds as cmds

"""
GROUP FINDER
"""


def isGroup(element):
    children = cmds.listRelatives(element, children=True)
    for child in children:
        if not cmds.ls(child, transforms=True):
            return False
    return True


class Values:
    def __init__(self):
        self.freezeTransform = True
        self.deleteHistory = True
        self.selectionOnly = False
        self.conformNormals = True
        self.rebuildNormals = True
        self.rebuildNormalOption = 0
        self.customNormalAngle = 60
        self.pivotOption = 1
        self.cleanUpMesh = True
        self.checkNonManyfold = True
        self.unityRefs = []
        self.alwaysOverrideExport = False
        self.displayInfo = True
        self.win = None