import maya.cmds as cmds
from Sanitizer import storage

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
    def __init__(self, freeze = True, delete = True, selectOnly = False, conform = True, rebuild = True, rebuildOption = 1, customAngle = 60, pivot = 1, clean = True, manyFold = True, override = False, info = True):
        self.freezeTransform = freeze
        self.deleteHistory = delete
        self.selectionOnly = selectOnly
        self.conformNormals = conform
        self.rebuildNormals = rebuild
        self.rebuildNormalOption = rebuildOption
        self.customNormalAngle = customAngle
        self.pivotOption = pivot
        self.cleanUpMesh = clean
        self.checkNonManyfold = manyFold
        self.alwaysOverrideExport = override
        self.displayInfo = info
        self.win = None

def setAllMetadata():
    cmds.editMetadata(streamName='freezeTransform', index=0, value=storage.values.freezeTransform, scene=True)
    cmds.editMetadata(streamName='deleteHistory', index=0, value=storage.values.deleteHistory, scene=True)
    cmds.editMetadata(streamName='selectionOnly', index=0, value=storage.values.selectionOnly, scene=True)
    cmds.editMetadata(streamName='conformNormals', index=0, value=storage.values.conformNormals, scene=True)
    cmds.editMetadata(streamName='rebuildNormals', index=0, value=storage.values.rebuildNormals, scene=True)
    cmds.editMetadata(streamName='rebuildNormalOption', index=0, value=storage.values.rebuildNormalOption, scene=True)
    cmds.editMetadata(streamName='customNormalAngle', index=0, value=storage.values.customNormalAngle, scene=True)
    cmds.editMetadata(streamName='pivotOption', index=0, value=storage.values.pivotOption, scene=True)
    cmds.editMetadata(streamName='cleanUpMesh', index=0, value=storage.values.cleanUpMesh, scene=True)
    cmds.editMetadata(streamName='checkNonManyfold', index=0, value=storage.values.checkNonManyfold, scene=True)
    cmds.editMetadata(streamName='alwaysOverrideExport', index=0,
                      value=storage.values.alwaysOverrideExport, scene=True)
    cmds.editMetadata(streamName='displayInfo', index=0, value=storage.values.displayInfo, scene=True)
    print(storage.unityRefDir)
    cmds.editMetadata(streamName='unityRefDir', index=0, stringValue=storage.unityRefDir, scene=True)