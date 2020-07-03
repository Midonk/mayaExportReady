# coding=utf-8
import os

"""
PROCESS NEEDED VALUES
"""
# stream names and value names paired with their struct
streams = {"freezeTransform": "sanBoolStruct",
           "deleteHistory": "sanBoolStruct",
           "selectionOnly": "sanBoolStruct",
           "conformNormals": "sanBoolStruct",
           "rebuildNormals": "sanBoolStruct",
           "rebuildNormalOption": "sanIntStruct",
           "customNormalAngle": "sanIntStruct",
           "pivotOption": "sanIntStruct",
           "exportResult": "sanBoolStruct",
           "exportAsOneObject": "sanBoolStruct",
           "exportFolder": "sanStringStruct",
           "exportExtension": "sanStringStruct",
           "exportName": "sanStringStruct",
           "unityRefDir": "sanStringStruct",
           "cleanUpMesh": "sanBoolStruct",
           "checkNonManyfold": "sanBoolStruct",
           "alwaysOverrideExport": "sanBoolStruct",
           "stayInScene": "sanBoolStruct",
           "displayInfo": "sanBoolStruct"}

# Expecting Value object
values = None

# Opened scene in Maya
scene = ""
sceneName = ""
sceneExt = ""

# Nodes retrieved from the scene
transformNodes = []
meshes = []
otherElement = []

"""
UI VARIABLES
"""

inShelfOffset = 10
shelfWidth = 381
globalColumnOffset = 5
globalRowOffset = 15
optionOffset = 10
titleHeight = 18
scrollRefWidth = 350

unityRefs = {}
prefsFile = os.path.join(os.path.dirname(__file__), "Prefs.json")
