# coding=utf-8
"""
main app core
"""

from imp import reload
import modules.ui_manager as ui
import modules.utility as utility
import modules.params as params
import modules.process as process

def reloadAll():
    reload(ui)
    reload(utility)
    reload(params)
    reload(process)

class Values:
    def __init__(self):
        self.freezeTransform = True
        self.deleteHistory = True
        self.conformNormals = True
        self.rebuildNormals = True
        self.rebuildNormalOption = 0
        self.customNormalAngle = 60
        self.pivotOption = 1
        self.cleanUpMesh = True
        self.checkNonManyfold = True
        self.unityRefs = []
        self.alwaysOverrideExport = False
        self.displayInfo = True
        self.win = None
values = Values()

# Launch app
def launchApp():
    reloadAll()
    values.win = ui.createWindow("Sanitizer", "params.getParams(values)", values)
