# Manually installing the Krita files

The Krita files should be installed automatically when you restart Comfy. Look in the python console for something like:

```
Edit with Krita files not installed, but the pykrita directory appears to be at ...\krita\pykrita.
Will try to install the files.
Edit with Krita files installed. You may need to restart Krita.
Edit in Krita using directory ...\pykrita\wait_and_open
```

In future runs, you should just see the last line.

If you see a message starting
```
***WARNING*** Edit with Krita - Default directory not located.
```
you may need to install the files manually. Or maybe Krita isn't installed.

To install manually:

- In Krita, go to the `Settings` menu and select `Manage Resources`. Then click the `Open Resource Folder` button.
- A file navigator window (or the equivalent in your OS) will open. In that folder, find the subfolder `pykrita`.
- Copy the folder `wait_and_open` and the file `wait_and_open.desktop` (from the krita_files subdirectory) into the `pykrita` subfolder.
- Make a note of the full path of the folder you just copied, ending `wait_and_open`
- Create a file in the custom node directory (`custom_nodes\cg-krita`) called `default.txt`, the first line of which is the folder path you just found. 
See default_example.txt for details.
- Restart Krita 
  - If you look in the `wait_and_open` directory, you should now see a file called `log.txt` has been created
- Restart Comfy

Still got problems? [Raise an issue](../issues)