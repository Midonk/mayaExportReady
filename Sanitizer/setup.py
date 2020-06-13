import maya.mel as mel
import maya.cmds as cmds
# import main.sanitizer as sanitizer

mainShelfLayout = mel.eval('global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;')
shelves = cmds.tabLayout(mainShelfLayout, q=True, childArray=True)

menuItem = cmds.optionMenu('tabMenu', q=True, value=True)
cmds.shelfButton(parent=mainShelfLayout + "|" + menuItem, label="Sanitizer" ''', image="playblast.png"''', sourceType='Python', command=command)