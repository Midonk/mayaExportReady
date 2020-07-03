import maya.mel as mel
import maya.cmds as cmds


# Create a permanent shortcut on a shelf in maya
def createShelf():
    # get the main shelf on the main window
    mainShelfLayout = mel.eval('global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;')
    command = '''
import Sanitizer.main as main
main.launchApp()
'''
    # Add the new tab to the main shelf
    mel.eval('addNewShelfTab ' + 'Sanitizer')
    cmds.shelfButton(parent=mainShelfLayout + "|" + 'Sanitizer', label="Sanitizer", image="playblast.png",
                     sourceType='Python', command=command)
