# coding=utf-8

import maya.cmds as cmds
from Sanitizer import storage


# Determine wether a transform is a group or not
# test if the transform node has a child of type "mesh"
def isMesh(node):
    if cmds.nodeType(node) == "mesh":
        return True

    childs = cmds.listRelatives(node, children=True)
    if childs:
        for child in childs:
            if cmds.nodeType(child) == "mesh":
                return True

    return False

    # children = cmds.listRelatives(element, children=True)
    # for child in children:
    #     if not cmds.ls(child, transforms=True):
    #         return False
    # return True


# The value object
class Values:
    def __init__(self, _freezeTransform=True, _deleteHistory=True, _selectionOnly=False, _conformNormals=True, _rebuildNormals=True, _rebuildNormalOption=1,
                 _customNormalAngle=60, _pivotOption=1, _cleanUpMesh=True, _checkNonManyfold=True, _alwaysOverrideExport=False, _displayInfo=False):
        self.freezeTransform = _freezeTransform
        self.deleteHistory = _deleteHistory
        self.selectionOnly = _selectionOnly
        self.conformNormals = _conformNormals
        self.rebuildNormals = _rebuildNormals
        self.rebuildNormalOption = _rebuildNormalOption
        self.customNormalAngle = _customNormalAngle
        self.pivotOption = _pivotOption
        self.cleanUpMesh = _cleanUpMesh
        self.checkNonManyfold = _checkNonManyfold
        self.alwaysOverrideExport = _alwaysOverrideExport
        self.displayInfo = _displayInfo
        self.win = None


# Update unityRef directory in metadata
def setUnityRefDir():
    cmds.editMetadata(streamName='unityRefDir', channelName='sanitizer', index=0, stringValue=storage.unityRefDir,
                      scene=True)


# Update all metadata
def setAllMetadata():
    for stream in storage.streams.keys():
        cmds.editMetadata(streamName=stream, channelName='sanitizer', index=0, value=getattr(storage.values, stream),
                          scene=True)

    setUnityRefDir()
