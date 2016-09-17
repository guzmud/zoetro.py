zoetro.py
=========

_.gif_ viewer in Python built on top of pyglet (_openGL_), using the native pyglet implementation of .gif loading into Animation and Sprite.

Requirements
------------
- Python 2.7
- pyglet

Modes
-----

- **fullscreen**: _zoetro.py_ can display the _.gif_ in its original size, adapted to the maximum size of the display, with a transparent background around the _.gif_ animation. In fullscreen, _zoetro.py_ will catch the whole screen and display a black background around the _.gif_ animation.
- **scaled**: while in fullscreen, _zoetro.py_ will leave the _.gif_ in its original size (minus the display size adaptation). If scaled, in fullscreen, _zoetro.py_ will scale the _.gif_ animation to one of the max dimension of the display maximum size.
- **loop**: _zoetro.py_ loads a _.gif_ in an animation, display it, then switch to the next one. If in loop mode, _zoetro.py_ will reload the same _.gif_ after the first display. Two sub-modes are available: __infinite-loop__ (where the same _.gif_ loops until the user manually switch to the next or previous _.gif_) and __k-loop mode__ (loop only k-times before switching to the next _.gif_).

Features
--------

- list the _.gif_ animations from a folder using the "_.gif_" extension and/or the GIF8 magic number
- randomize and un-randomize the _.gif_ animations list order while keeping the current _.gif_ as a pointer in the list
- configurable default display time for 1-frame _.gif_
- display size adaptation while rendering the _.gif_ animation
- switching mode does not break the display, nor reset the .gif animation, nor reset the loop count
- stackable mode (fullscreen-infinitely-looped-scaled-animation !)
- keyboard controls

Commands
--------

- **ESC**: close the window and quit the pyglet application
- **ENTER**: fullscreen mode on/off
- **LSHIFT**: scaled mode on/off
- **L**: loop mode on/off
- **R**: randomize the .gif animation list order
- **T**: reset the .gif animation list to the loading order
- **RIGHT**: display next gif in the current list order
- **LEFT**: display previous gif in the current list order

Arguments
---------

- **giffolder** (-gf, --giffolder): path to the .gif folder. Default variable and value: _giffolder = 'gifs'_
- **check\_ext** (-ext, --check\_ext): look for a ".gif" extension while checking if a file is a GIF file. Default variable and value: _check\_ext = True_
- **check\_hdr** (-hdr, --check\_ext): look for a GIF8 magic number in the file header wile checking if a file is a GIF file. Default variable and value: _check\_hdr = True_
- **fullscreen** (-f, --fullscreen): start directly in fullscreen mode. Default variable and value: _fullscreen = False_
- **scaled** (-s, --scaled): start directly in scaled mode. Default variable and value: _scaled = False_
- **loop** (-l, --loop): start directly in loop mode. Default variable and value: _loop = False_
- **loopnumber** (-ln, -loopnumber) : switch between infinite-loop mode and k-loop mode. Do not activate loop by default. Default variable and value: _loopnumber = None_
- **default\_time** (-dt, --default\_time): default time in s for 1-frame .gif file. Default variable and value: _default\_time = 1.1_

Future features
---------------

- recursive .gif loading, from the giffolder starting point then down the sub-folders
- configuration file, including arguments' default value and commands' key binding
- .gif animation and file information (path, name, duration, number of frames, etc.)