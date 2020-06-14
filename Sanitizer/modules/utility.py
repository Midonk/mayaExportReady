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
