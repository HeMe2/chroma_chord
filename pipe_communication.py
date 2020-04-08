import numpy
from openrazer.client.fx import Frame

pipe_name = "chroma_chord_pipe"

COLUMNS = 22
ROWS = 6
LEDs = COLUMNS * ROWS
BYTES_PER_VAL = 4


def read_frames(iterations: int):
    pipe = open(pipe_name, "rb")
    led_array = []
    for i in range(iterations):
        val = pipe.read(LEDs * BYTES_PER_VAL)
        led_values = []
        for ints in range(0, LEDs * BYTES_PER_VAL, BYTES_PER_VAL):
            rgb_as_one_num = int.from_bytes(val[ints:ints + BYTES_PER_VAL - 1], "big", signed=False)

            k = numpy.uint8((rgb_as_one_num & 0xFF000000) >> 24)
            r = numpy.uint8((rgb_as_one_num & 0x00FF0000) >> 16)
            g = numpy.uint8((rgb_as_one_num & 0x0000FF00) >> 8)
            b = numpy.uint8((rgb_as_one_num & 0x000000FF))

            led_values.append((k, r, g, b))
        led_array.append(led_values)
    pipe.close()
    return led_array


def print_as_frames(how_many: int, x: int = COLUMNS, y: int = ROWS):
    values = read_frames(how_many)
    for frame in values:
        for line_num in range(ROWS):
            line_start_index = line_num * x
            line_end_index = line_start_index + y
            print(frame[line_start_index: line_end_index])
        print("-------------------------------------------------------------------------------------------------------")


def read_razer_frames(number_of_frames: int = 1, pipe=None):
    pipe_was_none = pipe is None
    if pipe is None:
        pipe = open(pipe_name, "rb")

    frame_list = []
    for frame_num in range(number_of_frames):
        val = pipe.read(LEDs * BYTES_PER_VAL)
        frame = Frame((ROWS, COLUMNS))
        cur_row = 0
        cur_col = 0
        for index in range(0, LEDs * BYTES_PER_VAL, BYTES_PER_VAL):
            rgb_as_one_num = int.from_bytes(val[index:index + BYTES_PER_VAL - 1], "big", signed=False)
            r = numpy.uint8((rgb_as_one_num & 0xFF0000) >> 16)
            g = numpy.uint8((rgb_as_one_num & 0x00FF00) >> 8)
            b = numpy.uint8((rgb_as_one_num & 0x0000FF))

            if cur_col >= COLUMNS:
                cur_col = 0
                cur_row += 1

            frame.set(cur_row, cur_col, (r, g, b))
            cur_col += 1
        frame_list.append(frame)
    if pipe_was_none:
        pipe.close()
    return frame_list
