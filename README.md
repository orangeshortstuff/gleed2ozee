# gleed2ozee

A small tool for making levels for Ozee in Gleed2d, made in Python 3.

# Requirements
+ Python 3: https://www.python.org/downloads/

# Setting up a level
Make sure that gleed2ozee.py is in the same folder as any map you wish to convert (or the map is in a subfolder) otherwise the script **_will not be able_** to see the map.
After making a new layer:
+ Go to Textures > Choose, and select the "Ozee textures" folder
+ Copy the path, then go to the level, open the General tab, select and clear the ContentRootFolder, then paste in the path there

# Notes on placing objects
All textures in the folder are valid objects. The Wood, Ice, Rock, and Rubber textures convert to Box objects in game. Aside from the Coin, Checkpoint, and Door, all texture objects can be rotated and scaled and have those properties translate to the level - however, they are all considered static by default. (except for the Coin, which cannot be made static)

To make a moveable object, use the Rectangle or Circle primitives. These will be automatically converted into Box and Wheel objects respectively, with the Static flag set to false, and the material being Ice.

By default, 1 unit in Ozee is 105 pixels, and a 1x1 scale sprite is 4x4 units. Doors exit to (0, 0) at map 0 - the centre of the hub world, in vanilla.

# Converting from Gleed to Ozee
To make an Ozee compatible level, run gleed2ozee.py. On the first run, the program will ask for the name of the Gleed file, and then an output file.

Once these are inputted, the program will ask you whether to save these filenames or not. If you do choose to save them, they will save to a file "auto.txt" in the same folder as the Python script, at which point you can use a text editor to edit the names from there.

On further runs, the script automatically reads from auto.txt to get the source and destination file names. Please bear in mind that converting will **always** overwrite the previous contents of the file, so it may be worth keeping backups of the converted levels.

After converting the Gleed XML, the program appends a blob of Ozee XML from "include.txt" - use this if you want to add things to the level that the editor cannot yet do. (i.e signals or ropes)
