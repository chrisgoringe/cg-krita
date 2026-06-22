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
- In the custom node directory find (`default_example.txt`) and set PYKRITA_DIRECTORY to the `pykrita` directory full path, then rename that file to `default.txt`
- Restart Krita 
  - If you look in the `wait_and_open` directory, you should now see a file called `log.txt` has been created
- Restart Comfy

# Timing issues

On a slower hard drive, or for very large images, you might get issues when the wrong file appears, or the unmodified file is returned. 
You can try to reduce these issues by setting `PAD_TIME` in `default.txt` (see `default_example.txt` for instructions)

Still got problems? [Raise an issue](../issues)