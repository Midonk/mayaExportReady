import maya.mel as mel
import maya.cmds as cmds

def createShelf():
    mainShelfLayout = mel.eval('global string $gShelfTopLevel; string $tmp=$gShelfTopLevel;')
    # shelves = cmds.tabLayout(mainShelfLayout, q=True, childArray=True)
    command = '''
import Sanitizer.main as main
main.launchApp()
'''

    #menuItem = cmds.optionMenu('Sanitizer', width=200, enable=False)
    mel.eval('addNewShelfTab ' + 'Sanitizer')
    print(mainShelfLayout)
    cmds.shelfButton(parent=mainShelfLayout + "|" + 'Sanitizer', label="Sanitizer", image="playblast.png", sourceType='Python', command=command)
