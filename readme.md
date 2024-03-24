Windows Screen Recorder
=============================

Objective
---------
Small python script to record a rectangle desktop part at 60 fps using the Desktop Duplication API from Windows.

Usage
--------
Start program. Position of first mouse click after start is top left recording edge, second one bottom right edge of recording rectangle. Recording starts immediatly after bottom right mouse click.
Recording continues until left mouse click in upper left screen edge is performed (0,0). Video is stored besinde script in same folder encoded as XVID in avi.

Building .exe single-file with nuitka
-------------
```
python -m nuitka --standalone --onefile desktop_video.py
```
