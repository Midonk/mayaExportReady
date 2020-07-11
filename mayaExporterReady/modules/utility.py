# coding=utf-8

import maya.cmds as cmds
from mayaExporterReady import storage
import os
import json


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


# The value object
class Values:
    def __init__(self, _freezeTransform=True, _deleteHistory=True, _selectionOnly=False, _conformNormals=True,
                 _rebuildNormals=True, _rebuildNormalOption=1,
                 _customNormalAngle=60, _pivotOption=1, _exportResult=False, _exportFolder=None,
                 _exportAsOneObject=False, _exportExtension=None,
                 _exportName=None, _unityRefDir=None, _cleanUpMesh=True, _checkNonManyfold=True,
                 _alwaysOverrideExport=True, _stayInScene=True,
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
        sceneDir = os.path.dirname(cmds.file(q=True, sn=True))
        self.exportFolder = _exportFolder or os.path.dirname(
            os.path.dirname(cmds.about(env=True))) if sceneDir == "" else sceneDir
        self.exportAsOneObject = _exportAsOneObject
        self.exportExtension = _exportExtension or "exportFbx"
        self.exportName = _exportName or ""
        self.unityRefDir = _unityRefDir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "Refs")
        self.cleanUpMesh = _cleanUpMesh
        self.checkNonManyfold = _checkNonManyfold
        self.alwaysOverrideExport = _alwaysOverrideExport
        self.stayInScene = _stayInScene
        self.displayInfo = _displayInfo
        self.win = None


# Update unityRef directory in metadata
def setUnityRefDir():
    cmds.editMetadata(streamName='unityRefDir', channelName='mayaExporterReady', index=0,
                      stringValue=storage.values.unityRefDir,
                      scene=True)


def setExportFolder():
    cmds.editMetadata(streamName='exportFolder', channelName='mayaExporterReady', index=0,
                      stringValue=storage.values.exportFolder,
                      scene=True)


def setExportExtension():
    cmds.editMetadata(streamName='exportExtension', channelName='mayaExporterReady', index=0,
                      stringValue=storage.values.exportExtension,
                      scene=True)


def setExportName():
    cmds.editMetadata(streamName='exportName', channelName='mayaExporterReady', index=0, stringValue=storage.values.exportName,
                      scene=True)


# Update all metadata
def setAllMetadata():
    # print("Saving ALL metadata")
    for stream in storage.streams.keys():
        # print(stream, getattr(storage.values, stream))
        if storage.streams[stream] == "sanStringStruct":
            cmds.editMetadata(streamName=stream, channelName='mayaExporterReady', index=0,
                              stringValue=getattr(storage.values, stream),
                              scene=True)

        else:
            cmds.editMetadata(streamName=stream, channelName='mayaExporterReady', index=0,
                              value=getattr(storage.values, stream),
                              scene=True)


class JsonUtility():
    def __init__(self):
        pass

    @staticmethod
    def createJsonData():
        return {
            "freezeTransform": storage.values.freezeTransform,
            "deleteHistory": storage.values.deleteHistory,
            "selectionOnly": storage.values.selectionOnly,
            "conformNormals": storage.values.conformNormals,
            "rebuildNormals": storage.values.rebuildNormals,
            "rebuildNormalOption": storage.values.rebuildNormalOption,
            "customNormalAngle": storage.values.customNormalAngle,
            "pivotOption": storage.values.pivotOption,
            "exportResult": storage.values.exportResult,
            "exportFolder": storage.values.exportFolder,
            "exportAsOneObject": storage.values.exportAsOneObject,
            "exportExtension": storage.values.exportExtension,
            "exportName": storage.values.exportName,
            "unityRefDir": storage.values.unityRefDir,
            "cleanUpMesh": storage.values.cleanUpMesh,
            "checkNonManyfold": storage.values.checkNonManyfold,
            "alwaysOverrideExport": storage.values.alwaysOverrideExport,
            "stayInScene": storage.values.stayInScene,
            "displayInfo": storage.values.displayInfo,
        }

    @staticmethod
    def read(path):
        with open(path, "r") as file:
            # read
            data = file.read()
            # parse
            return json.loads(data)

    @staticmethod
    def write(path, data):
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)


def createPrefs():
    # print("Creation of the prefs file")
    open(storage.prefsFile, "a")
    settings = JsonUtility.createJsonData()
    JsonUtility.write(storage.prefsFile, settings)
