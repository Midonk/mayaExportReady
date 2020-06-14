# coding=utf-8
"""
main app core
"""

from imp import reload
import maya.cmds as cmds
import os
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
    streamsName = storage.streams.keys()

    if cmds.hasMetadata(channelName='sanitizer', scene=True)[0]:
        storage.values = utility.Values()
        for stream in streamsName:
            setattr(storage.values, stream, cmds.getMetadata(streamName=stream, index=0, scene=True)[0])

        storage.unityRefDir = cmds.getMetadata(streamName="unityRefDir", index=0, scene=True)[0]

    else:
        print("Creation of metadata")
        cmds.dataStructure(format='raw', asString='name=sanBoolStruct:bool=value')
        cmds.dataStructure(format='raw', asString='name=sanIntStruct:int32=value')
        cmds.dataStructure(format='raw', asString='name=sanStringStruct:string=value')

        for stream in streamsName:
            cmds.addMetadata(structure=storage.streams[stream],
                             streamName=stream,
                             channelName='sanitizer',
                             scene=True)

        cmds.addMetadata(structure="sanStringStruct",
                         streamName="unityRefDir",
                         channelName='sanitizer',
                         scene=True)

        storage.values = utility.Values()
        storage.unityRefDir = os.path.join(os.path.dirname(os.path.dirname(cmds.about(env=True))),
                                           "scripts/Sanitizer/Refs")

    utility.setAllMetadata()



# Launch app
def launchApp():
    reloadAll()
    initialize()
    storage.values.win = ui.createWindow("Sanitizer", lambda command: params.getParams())
