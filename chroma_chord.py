#!/usr/bin/python3
"""
Computer audio to light conversion for Razer RGB keyboards on Linux.

Copyright (C) 2020 Henning Mende

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""


from threading import Thread
from subprocess import call
import pipe_communication as pc
import openrazer.client
from openrazer.client import constants as razer_constants
import time


__author__ = "Henning Mende"
__copyright__ = "Copyright 2020, Chroma Chord"
__licence__ = "GPL-3.0-or-later"
__email__ = "github@skotax.de"


class Timer:
    def __init__(self):
        self.start = time.time()

    def reset(self):
        self.start = time.time()

    def get_time(self):
        return time.time() - self.start


def values_from_pipe_to_keyboard(device):
    global colorchord_active
    current_frame = pc.read_razer_frames(1)[0]

    if not is_frame_completely_black(current_frame):
        timer.reset()

    if timer.get_time() > threshold and colorchord_active:
        colorchord_active = False
        device.fx.starlight_random(razer_constants.STARLIGHT_NORMAL)
    elif timer.get_time() < threshold:
        colorchord_active = True
        device.fx.advanced.matrix = current_frame
        # set the color of the "alt gr" also for the razer logo, because the logo
        # is located in the matrix on the top right corner, while it is physically nearer to the
        # "alt gr" key.
        color_alt_gr = device.fx.advanced.matrix.get(5, 11)
        device.fx.advanced.matrix.set(0, 20, color_alt_gr)

        device.fx.advanced.draw()


def is_frame_completely_black(frame):
    return sum(sum(sum(frame._matrix))) == 0


def get_keyboard():
    device_list = openrazer.client.DeviceManager().devices
    key_board = None

    for device in device_list:
        if device.type == "keyboard":
            key_board = device

    return key_board


def chroma_chord_operation():
    pass


if __name__ == "__main__":

    attempts = 30
    keyboard = get_keyboard()

    try:
        while keyboard is None and attempts > 0:
            keyboard = get_keyboard()
            time.sleep(10)
            attempts -= 1
    except KeyboardInterrupt:
        pass

    if keyboard is not None:
        # chroma_chord_operation()
        print("start ColorChord 2")

        colorchord_start = lambda: call(
            ["./colorchord"] + ["chroma_chord_voronoi.conf"]
        )  # TODO: fix this later
        colorchord_thread = Thread(name="ChromaChord", target=colorchord_start)
        colorchord_thread.setDaemon(True)
        colorchord_thread.start()

        timer = Timer()
        threshold = 3  # threshold in seconds until standby animation starts
        colorchord_active = True

        pipe = open(pc.pipe_name, "rb")  # TODO move pipe name out of pipe_communication

        try:
            while True:
                values_from_pipe_to_keyboard(keyboard)
                # pc.print_as_frames(1)
        except KeyboardInterrupt:
            print("\nstop")
        finally:
            keyboard.fx.starlight_random(razer_constants.STARLIGHT_NORMAL)
            pipe.close()

    else:
        print("No keyboard found!")
