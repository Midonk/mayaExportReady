# coding=utf-8

from imp import reload
import maya.cmds as cmds
import os
import storage
import modules.ui_manager as ui
import modules.utility as utility
import modules.params as params
import modules.process as process


# DEV
# reload all modules to refresh them
def reloadAll():
    reload(ui)
    reload(utility)
    reload(params)
    reload(process)
    reload(storage)


# Retrieve value from metadata and set to values
# or create them if they doesn't exists and initialize them
def initialize():
    streamsName = storage.streams.keys()

    # retrieve metadata
    if cmds.hasMetadata(channelName='sanitizer', scene=True)[0]:
        print("Retrieve metadata")
        storage.values = utility.Values()
        for stream in streamsName:
            print(stream, cmds.hasMetadata(streamName=stream, channelName='sanitizer', scene=True))
            setattr(storage.values, stream, cmds.getMetadata(streamName=stream, channelName='sanitizer', index=0, scene=True)[0])

        storage.unityRefDir = cmds.getMetadata(streamName="unityRefDir", index=0, scene=True)[0]

    # create metadata
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

    # Apply metadata values on the scene
    utility.setAllMetadata()


# Launch app
def launchApp():
    reloadAll()
    initialize()
    storage.values.win = ui.createWindow("Sanitizer", lambda command: params.getParams())
