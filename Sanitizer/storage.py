
"""
PROCESS NEEDED VALUES
"""
streams = {"freezeTransform":"sanBoolStruct",
            "deleteHistory":"sanBoolStruct",
            "selectionOnly":"sanBoolStruct",
            "conformNormals":"sanBoolStruct",
            "rebuildNormals":"sanBoolStruct",
            "rebuildNormalOption":"sanIntStruct",
            "customNormalAngle":"sanIntStruct",
            "pivotOption":"sanIntStruct",
            "cleanUpMesh":"sanBoolStruct",
            "checkNonManyfold":"sanBoolStruct",
            "alwaysOverrideExport":"sanBoolStruct",
            "displayInfo":"sanBoolStruct"}

values = None

scene = ""
transformNodes = []
meshes = []
groups = []


"""
UI VARIABLES
"""

inShelfOffset = 10
shelfWidth = 295
globalColumnOffset = 5
globalRowOffset = 15
optionOffset = 10

unityRefDir = ""
unityRefs = {}