# coding=utf-8
"""
main app core
"""

from imp import reload
import storage
import modules.ui_manager as ui
import modules.utility as utility
import modules.params as params
import modules.process as process


def reloadAll():
    reload(ui)
    reload(utility)
    reload(params)
    reload(process)
    reload(storage)


# Retrieve value from metadata and set to values
def initialize():
    pass


# Launch app
def launchApp():
    reloadAll()
    storage.values.win = ui.createWindow("Sanitizer", lambda command: params.getParams())
