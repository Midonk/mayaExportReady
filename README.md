# MayaExporterReady
## In short:
The 'Sanitizer' script has been created to allow you tu prepare your scene and meshes to be exported. 
If you want it, the script can also export your scene as '.obj' or '.fbx'

This script has been designed for game developpers but can also be really helpful for other people

## Installing the script:
1. Set the 'mayaExporterReady' folder into 'Documents\maya\scripts' folder
1. Open Maya
1. Open the console at the bottom right of your screen "{;}"
1. Set the console to Python (in Python by default)
1. Copy paste those two lines into the console
    ```python
    import Sanitizer.setup as setup
    setup.createShelf()
    ```
1. Press **CTRL + Enter**
1. Click on the button in the new shelf that just appears names "Sanitizer"

┏(＾0＾)┛ **You are done** (~‾▿‾)~

## What the script does:
- **Give a clear UI** allowing the user to manage the process options of the script
- **Create an export duplication** of your scene to prevent destructive actions on your work scene
- **Remind of your preceding options** per scenes making you gain time <br>
    *NOTE: the script uses metadata that are generally saved when you launch the script.*
- You can **save your settings as preferences** to make your own settings as the default ones in every projects
- You can **reset the setting of the window** at any time following your preferences

## What the script can do:
- **Freeze transformations** of all type of transform nodes
- **Delete the history** of all type of transform nodes
- Constraint its process on your **selection or on the all scene**
- **Make a cleanup** of your meshes
- **Check non-manifold meshes** and display some informations about it
- **Conform normals** of your meshes
- **Rebuild normals** of your meshes with given angles
- **Relocalize your pivot**
- **Export the result** of the process as FBX or OBJ
- **Export your scene or selection as one** file
- **Search and import reference** meshes directly into your scene
- **Display informations** about the script process

## What the script don't do
- As the script check for non-manifold meshes, it's still up to you to clean them up. <br>
  NOTE: The process gives you informations about the problematic elements