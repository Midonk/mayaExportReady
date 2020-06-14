import modules.utility as utility
import maya.cmds as cmds
import os

"""
PROCESS NEEDED VALUES
"""

values = utility.Values()
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

unityRefDir = os.path.join(os.path.dirname(os.path.dirname(cmds.about(env=True))),
                           "scripts/Sanitizer/Refs")
unityRefs = {}