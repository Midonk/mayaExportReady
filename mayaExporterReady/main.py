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

    # check for existing prefs file
    if os.path.isfile(storage.prefsFile):
        # print("Prefs file exists")
        prefs = utility.JsonUtility.read(storage.prefsFile)

        for stream in streamsName:
            setattr(storage.values, stream, prefs[stream])

    # create a new prefs file
    else:
        # print("Prefs file don't exist")
        utility.createPrefs()

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

    # Create all on first utilisation
    if not cmds.hasMetadata(channelName='sanitizer', scene=True)[0]:
        print("Creation of the metadata")
        for stream in streamsName:
            # create
            cmds.addMetadata(structure=storage.streams[stream],
                             streamName=stream,
                             channelName='sanitizer',
                             scene=True)
    # Retrieve or create
    else:
        print("Retrieve the metadata")
        for stream in streamsName:
            # create
            if not cmds.hasMetadata(streamName=stream, channelName='sanitizer', scene=True)[0]:
                # print(stream + " => create")
                cmds.addMetadata(structure=storage.streams[stream],
                                 streamName=stream,
                                 channelName='sanitizer',
                                 scene=True)

            # retrieve
            else:
                setattr(storage.values, stream,
                        cmds.getMetadata(streamName=stream, channelName='sanitizer', index=0, scene=True)[0])
                # print(stream + " " + str(getattr(storage.values, stream)) + " => exists")

    # check if the directories path are valid (preventing scene exchange with wrong metadatas)
    if not os.path.isdir(storage.values.exportFolder):
        print("is not dir")
        storage.values.exportFolder = os.path.dirname(os.path.dirname(cmds.about(env=True)))

    if not os.path.isdir(storage.values.unityRefDir):
        print("is not dir")
        storage.values.unityRefDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Refs")

    # Apply metadata values on the scene
    utility.setAllMetadata()


# Launch app
def launchApp():
    reloadAll()
    initialize()
    storage.values.win = ui.createWindow("Sanitizer", lambda command: params.launchScript())
