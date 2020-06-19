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
    storage.values = utility.Values()
    # Check for datastructure statements
    datastructures = cmds.dataStructure(q=True)
    if not "sanBoolStruct" in datastructures:
        print("Create sanBoolStruct")
        cmds.dataStructure(format='raw', asString='name=sanBoolStruct:bool=value')
    if not "sanIntStruct" in datastructures:
        print("Create sanIntStruct")
        cmds.dataStructure(format='raw', asString='name=sanIntStruct:int32=value')
    if not "sanStringStruct" in datastructures:
        print("Create sanStringStruct")
        cmds.dataStructure(format='raw', asString='name=sanStringStruct:string=value')

    if not cmds.hasMetadata(channelName='sanitizer', scene=True)[0]:
        print("Creation of the metadata")
        for stream in streamsName:
            # create
            cmds.addMetadata(structure=storage.streams[stream],
                             streamName=stream,
                             channelName='sanitizer',
                             scene=True)

    else:
        print("Retrieve the metadata")
        # Retrieve or create
        print("Read streams")
        for stream in streamsName:
            # create
            if not cmds.hasMetadata(streamName=stream, channelName='sanitizer', scene=True)[0]:
                print(stream + " => create")
                cmds.addMetadata(structure=storage.streams[stream],
                                 streamName=stream,
                                 channelName='sanitizer',
                                 scene=True)

            # retrieve
            else:
                setattr(storage.values, stream,
                        cmds.getMetadata(streamName=stream, channelName='sanitizer', index=0, scene=True)[0])
                print(stream + " " + str(getattr(storage.values, stream)) + " => exists")

    # Apply metadata values on the scene
    utility.setAllMetadata()


# Launch app
def launchApp():
    reloadAll()
    initialize()
    storage.values.win = ui.createWindow("Sanitizer", lambda command: params.getParams())
