# mayaToUnityReady
## When launched
- **make all the action a single history element** 
```python
cmds.undoInfo(cn="nomDeChunk", ock=True)

..... #content

cmds.undoInfo(cn="nomDeChunk", cck=True)
```

- scale the objects with unity scale (if user want) 
(give reference to the user as a template (not exported or anything))
OR
give the possibility to the user to give a path to a reference of objects

## For every objects in the scene
check for
- freeze transform
    - if not frozen => ask user if he want the program to do it
        - if yes, the program does it
        ```python
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        ```
        - else continue without incremet progress bar

- delete history
    - if not deleted, ask the user if he wish to delet it
        - if yes, delete it
        ```python   
        cmds.delete(constructionHistory=True)
        ```
        - else continue without increment the progress bar

- check normals
```python
cmds.polyNormal(mn=2)
```

- set pivot of the mesh on maya pivot (if user want)(bake pivot)
add options  (radio)
    - pas toucher
    - centre de la scene
    - centre de l'objet

- check obj & fbx plugins are activated 
```python
cmds.pluginInfo("name", ...)
``` 
- clean up
```python
cmds.polyClean()
```

- progress bar

- non manyfold => polyInfo (warning)
```python
cmds.polyInfo()
```



faire une copie du fichier à exporter et travailler sur le duplicatat

vers la fin (wishlist)
mettre les données d'exports le fichier original en tant que métadonnée
à chaque lancement du script, il check les métadonnées et paramètre la box en fonction de ce qu'il trouve

#Plan

##Ouverture de la fenêtre
1. Lecture des métadonnées pour paramétrer les préférences utilisateur
1. afficher la fenêtre

##Plus
- spawn reference object in the active scene
    - by default it spawn a unit cube from Unity
    - The user can specify a directory to spawn listed meshes in it


##Lancement de la procédure d'export

1. **Avertissement de l'utilisateur sur ce qui va se passer si les infos sont activées => proposer de les désactiver**
1. écriture des métadonnées dans le projet selon les choix des paramètres d'export
1. Vérification qu'il n'existe pas de fichier au nom du projet + '_export'
    - suppression du fichier / override
1. Duplication du projet dans le dossier de la source avec le suffixe '_export'
1. ouverture du projet dans maya
1. récupération des meshs à exporter
1. freeze les transformations
1. delete l'history
1. conformer les normales
1. Positionner les pivots en fonctions des préférences
1. clean up
1. tell the user everything has been applied