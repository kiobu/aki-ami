# AMI

AMI, or AutoModInstaller, is a tool to automagically install SPT-AKI mods that support the AMI metadata format, 
described below.

This allows easier mod installation for users if mod authors choose to structure their mod in an AMI-compliant format.
Non-AMI-compliant mods will not work with the AMI tool.

# AMI Metadata Format

The AMI (.ami) format is simply JSON with specific keys and values. Note that mod authors wishing to use the AMI format
**must** name their ami file *metadata.ami*.

```js
{
    "metadata": {
        "mods": [
            {
                "type": "client",
                "path_to_root": "/clientmod/"
            },
            {
                "type": "server",
                "path_to_root": "/servermod/"
            }
        ]
    }
}
```

The `metadata` object is the root object for AMI-compliant metadata files.

The `mods` array is an array of all "root" mod directories. This means any individual mods that would go into one of 
the following locations:

```
aki-dir/
|
|__ server/
|  |
|  |__ user/
|     |
|     |__ mods/ <-- 'server' type root folder
|
|__ client/ <-- 'client' type root folder
   |
   |__ EscapeFromTarkov.exe
   |
   |__ BepInEx/
```

See the [example mod](example_mod/) folder for a properly formatted AMI-compliant mod.

The `type` property of a `mod` designates the type of mod to be installed. This can only be `client` or `server`.

The `path_to_root` property of a `mod` is the relative path to the server or client mod source. 

For clients, the mod will be installed to ***{aki-dir}**/client/*, and server mods to ***{aki-dir}**/server/user/mods*.

Note that the folder name and, ergo, the `path_to_root` for a server mod should be what you want the name of
your mod folder to be in ***{aki-dir}**/server/user/mods*.

This is in contrast to the average client mod, as the majority of these mods are BepInEx plugins. As
such, the corresponding `path_to_root` folder (the mod folder) must have a *BepInEx/* folder. This was designed to be one directory level
backwards in case any client modders wanted to access ***{aki-dir}**/client/Aki_Data* or some other game-level folder.

Any violations of the AMI format should be caught by the AMI validator, which will prevent mods with malformed
AMI metadatas from being installed.

# Building

**Required:** Python 3.9, poetry

To build, set up your Poetry environment, and run `poetry run pyinstaller --onefile src/app.py --collect-submodules application --name aki-ami`.