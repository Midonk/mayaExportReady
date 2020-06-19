# coding=utf-8

import maya.cmds as cmds
from Sanitizer import storage
import os


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
    def __init__(self, _freezeTransform=True, _deleteHistory=True, _selectionOnly=False, _conformNormals=True,
                 _rebuildNormals=True, _rebuildNormalOption=1,
                 _customNormalAngle=60, _pivotOption=1, _exportResult=False, _exportFolder=None, _exportExtension=None,
                 _exportName=None, _cleanUpMesh=True, _checkNonManyfold=True, _alwaysOverrideExport=False,
                 _displayInfo=False):
        self.freezeTransform = _freezeTransform
        self.deleteHistory = _deleteHistory
        self.selectionOnly = _selectionOnly
        self.conformNormals = _conformNormals
        self.rebuildNormals = _rebuildNormals
        self.rebuildNormalOption = _rebuildNormalOption
        self.customNormalAngle = _customNormalAngle
        self.pivotOption = _pivotOption
        self.exportResult = _exportResult
        scenePath = cmds.file(q=True, sn=True)
        self.exportFolder = _exportFolder or os.path.dirname(
            os.path.dirname(cmds.about(env=True))) if scenePath == "" else scenePath
        self.exportExtension = _exportExtension or "exportFbx"
        self.exportName = _exportName or "myMesh"
        self.cleanUpMesh = _cleanUpMesh
        self.checkNonManyfold = _checkNonManyfold
        self.alwaysOverrideExport = _alwaysOverrideExport
        self.displayInfo = _displayInfo
        self.win = None


# Update unityRef directory in metadata
def setUnityRefDir():
    cmds.editMetadata(streamName='unityRefDir', channelName='sanitizer', index=0, stringValue=storage.unityRefDir,
                      scene=True)


def setExportFolder():
    cmds.editMetadata(streamName='exportFolder', channelName='sanitizer', index=0,
                      stringValue=storage.values.exportFolder,
                      scene=True)


def setExportExtension():
    cmds.editMetadata(streamName='exportExtension', channelName='sanitizer', index=0,
                      stringValue=storage.values.exportExtension,
                      scene=True)


def setExportName():
    cmds.editMetadata(streamName='exportName', channelName='sanitizer', index=0, stringValue=storage.values.exportName,
                      scene=True)


# Update all metadata
def setAllMetadata():
    print("Saving ALL metadata")
    for stream in storage.streams.keys():
        print(stream, getattr(storage.values, stream))
        if storage.streams[stream] == "sanStringStruct":
            cmds.editMetadata(streamName=stream, channelName='sanitizer', index=0,
                              stringValue=storage.values.exportFolder,
                              scene=True)

        else:
            cmds.editMetadata(streamName=stream, channelName='sanitizer', index=0,
                              value=getattr(storage.values, stream),
                              scene=True)

    setUnityRefDir()
