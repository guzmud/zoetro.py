#!/usr/bin/python

import os
import sys
import io
import random
import argparse

import pyglet  # todo: check compatibility according to pyglet version

# zoetro.py global parameters
giffolder = 'gifs'  # default folder is a local ./gifs/ folder (string)
check_ext = True  # check if '.gif' is at the end of the filename (boolean)
check_hdr = True  # check if 'GIF8' is the file header (boolean)
fullscreen = False  # not in fullscreen by default (boolean)
scaled = False  # unscaled .gif by default (boolean)
loop = False  # looping on the same .gif by default (boolean)
loopnumber = None  # infinite-loop (None) or k-loop (some int), when required
default_time = 1.1  # default time in s for non-animated/one-frame gif (float)

# zoetro.py global variables
gifargs = list()
giflist = None
gifptr = 0  # current index in giflist
loopptr = 0  # current index in case of loopnumber
scaling_factor = 1
gif_anim = None
gif_sprite = None
gifsize = (0, 0)

# pyglet-related parameters and variables
screen = pyglet.window.get_platform().get_default_display().get_screens()[0]
screensize = (screen.width, screen.height)
bgcolor = (0, 0, 0)  # R,G,B from 0 to 1 (float)
window = None

# wip
gif_label = pyglet.text.Label()  # wip


# redefine the on_animation_end function to manage loop
def on_animation_end():
    global loopptr

    if not loop:
        next_gif()
    elif loopnumber is not None:
        loopptr += 1
        if not(loopptr < loopnumber):
            next_gif()


def next_gif():
    global gifptr
    gifptr = (gifptr+1) % len(giflist)
    load_gif()


def previous_gif():
    global gifptr
    gifptr = (gifptr-1) % len(giflist)
    load_gif()


# used with argparser
def thats_the_question(element):

    positive = ['true', 'yes', 't', 'y']
    negative = ['false', 'no', 'f', 'n']

    if element in positive:
        return True
    elif element in negative:
        return False
    else:
        return None


def load_arguments():
    global gifargs, giffolder, check_ext, check_hdr
    global fullscreen, scaled, loop, default_time, loopnumber

    # argparse configuration
    parser = argparse.ArgumentParser(
        description="Gif viewer in Python based on openGL/pyglet.",
        epilog='In Python we trust.')

    parser.add_argument('-gf', '--giffolder',
                        help="path to .gif folder"
                        " [path] [local default: "+giffolder+"]")
    parser.add_argument('-ext', '--check_ext',
                        help="check for a .gif extension before loading"
                        " [true/false] [local default: "+str(check_ext)+"]")
    parser.add_argument('-hdr', '--check_hdr',
                        help="check for an in-file GIF8 header"
                        " [true/false] [local default: "+str(check_hdr)+"]")
    parser.add_argument('-f', '--fullscreen',
                        help="start in fullscreen mode"
                        " [true/false] [local default: "+str(fullscreen)+"]")
    parser.add_argument('-s', '--scaled',
                        help="start in scaled mode"
                        " [true/false] [local default: "+str(scaled)+"]")
    parser.add_argument('-l', '--loop',
                        help="start in loop mode"
                        " [true/false] [local default: "+str(loop)+"]")
    parser.add_argument('-ln', '--loopnumber',
                        help="switch from infinite-loop to k-loop in loop mode"
                        " [int] [local default: "+str(loopnumber)+"]")
    parser.add_argument('-dt', '--default_time',
                        help="default time in s for 1-frame .gif"
                        " [float] [local default: "+str(default_time)+"]")
    gifargs = parser.parse_args()

    # inputs management
    if gifargs.giffolder is not None:
        giffolder = gifargs.giffolder

    if gifargs.check_ext is not None:
        boolval = thats_the_question(gifargs.check_ext.lower())
        if boolval in [True, False]:
            check_ext = boolval

    if gifargs.check_hdr is not None:
        boolval = thats_the_question(gifargs.check_hdr.lower())
        if boolval in [True, False]:
            check_hdr = boolval

    if gifargs.fullscreen is not None:
        boolval = thats_the_question(gifargs.fullscreen.lower())
        if boolval in [True, False]:
            fullscreen = boolval

    if gifargs.scaled is not None:
        boolval = thats_the_question(gifargs.scaled.lower())
        if boolval in [True, False]:
            scaled = boolval

    if gifargs.loop is not None:
        boolval = thats_the_question(gifargs.loop.lower())
        if boolval in [True, False]:
            loop = boolval

    if gifargs.loopnumber is not None:
        dln = ''.join([x for x in gifargs.loopnumber if x in "0123456789"])
        if dln is not '':
            loopnumber = int(dln)

    if gifargs.default_time is not None:
        dt = ''.join([x for x in gifargs.default_time if x in "0123456789."])
        if dt is not '':
            default_time = float(dt)


def test_gif(gifpath):
    isgif = True

    # is it a file ?
    if not os.path.isfile(gifpath):
        isgif = False

    # is it a '.gif' file ? (and do we care)
    if (gifpath[-4:] != '.gif' and check_ext) and isgif:
        isgif = False

    # is it a file with a 'GIF8' header ? (and do we care)
    if check_hdr and isgif:
        with io.open(gifpath, 'rb') as f:
            if f.read(4) != 'GIF8':
                isgif = False

    return isgif


def load_folder():
    global giflist, giffolder, gifptr

    try:
        giflist = [os.path.join(giffolder, f)
                   for f in os.listdir(giffolder)
                   if test_gif(os.path.join(giffolder, f))]
    except:
        raise ValueError('giffolder is not a valid path')

    gifptr = 0


def get_current_gif():
    return giflist[gifptr]


def randomize_list():
    global giflist, gifptr

    gifname = get_current_gif()
    random.shuffle(giflist)
    gifptr = giflist.index(gifname)


def reset_list():
    global gifptr

    gifname = get_current_gif()
    load_folder()
    gifptr = giflist.index(gifname)


def load_gif():
    global gif_anim, gif_sprite, gif_label, giflist, gifptr, loopptr, window

    # get the gif file, load it as an animation, put the animation in a sprite
    gifname = get_current_gif()

    try:
        gif_anim = pyglet.image.load_animation(gifname)
    except pyglet.image.codecs.ImageDecodeException:
        giflist.pop(gifptr)
        gifptr = (gifptr-1) % len(giflist)
        next_gif()
    except:
        giflist.pop(gifptr)
        gifptr = (gifptr-1) % len(giflist)
        next_gif()
    # does it need to be delete / garbage collected like the gif_sprite ?

    if len(gif_anim.frames) == 1:
        gif_anim.frames = [pyglet.image.AnimationFrame(x.image, default_time)
                           for x in gif_anim.frames]

    # proper garbage collection for Sprite objects
    if gif_sprite:
        gif_sprite.delete()

    gif_sprite = pyglet.sprite.Sprite(gif_anim)
    gif_sprite.on_animation_end = on_animation_end
    gif_sprite.set_position(0, 0)

    # force the scaling factor at 1 before decision
    # (global variable and sprite parameter)
    reset_scale()

    if fullscreen:
        window.set_fullscreen(fullscreen)
        scale_decision()

    if loopnumber is not None:
        loopptr = 0

    position_window()
    position_gif()

    show_label()  # wip


# wip
def show_label():
    global gif_label

    gifname = get_current_gif()

    if fullscreen:
        tx = screensize[0]/2.00
    else:
        tx = gifsize[0]/2.00

    gif_label = pyglet.text.Label(text=gifname,
                                  x=tx,
                                  anchor_x='center')


def position_window():
    global fullscreen, gifsize, screensize, window

    if not fullscreen:
        window.set_size(gifsize[0], gifsize[1])
        window.set_location(int(screensize[0]/2.00-gifsize[0]/2.00),
                            int(screensize[1]/2.00-gifsize[1]/2.00))


def position_gif():
    global fullscreen, gif_sprite, screensize, gifsize

    if fullscreen:
        gif_sprite.position = (int(screensize[0]/2.00-gifsize[0]/2.00),
                               int(screensize[1]/2.00-gifsize[1]/2.00))
    else:
        gif_sprite.position = (0, 0)


def scale_gif():
    global gif_sprite, scaling_factor, gifsize, screensize
    gif_sprite.scale = 1

    scaling_factor = min(screensize[0]*1.00/gifsize[0],
                         screensize[1]*1.00/gifsize[1])

    gif_sprite.scale = scaling_factor


def reset_scale():
    global gif_sprite, scaling_factor, gifsize
    scaling_factor = 1
    gif_sprite.scale = scaling_factor
    gifsize = (gif_sprite.width,
               gif_sprite.height)


def scale_decision():
    global gif_sprite, gifsize, fullscreen

    if scaled and fullscreen:
        scale_gif()
    else:
        reset_scale()

    gifsize = (gif_sprite.width,
               gif_sprite.height)
    position_gif()


def switch_scaled():
    global scaled
    scaled = not scaled


def switch_loop():
    global loop
    loop = not loop


def post_fullscreen():
    scale_decision()
    position_gif()
    position_window()
    show_label()


def switch_fullscreen():
    global fullscreen, window
    fullscreen = not fullscreen
    window.set_fullscreen(fullscreen)


def main(argv=None):
    global window
    winstyle = pyglet.window.Window.WINDOW_STYLE_BORDERLESS
    window = pyglet.window.Window(fullscreen=False,
                                  style=winstyle,)

    load_arguments()
    load_folder()
    load_gif()

    @window.event
    def on_draw():
        window.clear()
        gif_sprite.draw()
        gif_label.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        # ESCAPE: quit
        if symbol == pyglet.window.key.ESCAPE:
            window.close()  # more to do in order to shutdown properly ?
            return 0

        # ENTER : fullscreen on/off
        elif symbol == pyglet.window.key.ENTER:
            switch_fullscreen()
            post_fullscreen()

        # LEFT SHIFT: scale gif to screensize on/off
        elif symbol == pyglet.window.key.LSHIFT:
            switch_scaled()
            scale_decision()

        # L : looping on the same gif on/off
        elif symbol == pyglet.window.key.L:
            switch_loop()

        # R : randomize the giflist order
        elif symbol == pyglet.window.key.R:
            randomize_list()

        # T : reset the giflist order ('un-randomize')
        elif symbol == pyglet.window.key.T:
            reset_list()

        # RIGHT : next gif in list
        elif symbol == pyglet.window.key.RIGHT:
            next_gif()

        # LEFT : previous gif in list
        elif symbol == pyglet.window.key.LEFT:
            previous_gif()

    pyglet.gl.glClearColor(bgcolor[0], bgcolor[1], bgcolor[2], 1)
    pyglet.app.run()

    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
