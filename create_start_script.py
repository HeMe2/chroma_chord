#!/usr/bin/python3
import os

_wrong_platform_msg = """Error: Not on Linux platform.
This software won't run on anything else than linux...
Sorry, not sorry!"""
_openrazer_missing_msg = """Error: Dependency not satisfied: openrazer
You need to install the open razer services (https://openrazer.github.io/)"""
_colorchord_missing_msg = """Error: Dependency not satisfied: colorchord
You need to compile your colorchord for linux and move the executable to this directory!
Follow the compilation instructions on https://github.com/cnlohr/colorchord, for the colorchord2 project!"""
_no_sourcename_msg = """Error: No sourcename specified in chroma_chord_voronoi.conf.
For Linux mostly use the following command to find valid devices to read from: 
pactl list | grep pci- | grep monitor
Or just: ` pactl list | grep monitor ` if you're using an USB soundcard or something similar.
Then add the line:
sourcename = <device_name>
to chroma_chord_voronoi.conf"""


def check_platform()->bool:
    import platform
    if platform.system() == "Linux":
        return True
    else:
        print(_wrong_platform_msg)
        return False
        # further checks are obsolete
        return dependencies_satisfied


def check_openrazer() -> bool:
    openrazer_found = True
    try:
        import openrazer
    except ImportError:
        print(_openrazer_missing_msg)
        openrazer_found = False
    return openrazer_found


def check_colorchord() -> bool:
    filename = "./colorchord"
    if os.path.isfile(filename) and os.access(filename, os.X_OK):
        return True
    else:
        print(_colorchord_missing_msg)
        return False


def check_sourcename() -> bool:
    sourcename_configured = False
    with open("chroma_chord_voronoi.conf", "r") as conf_file:
        for line in conf_file:
            if (not (line.find("sourcename") == -1)) and (line.find("#sourcename") == -1):
                # line contains "sourcename" but not "#sourcename" (which is a comment)
                sourcename_configured = True
    if not sourcename_configured:
        print(_no_sourcename_msg)
    return sourcename_configured


def check_dependencies() -> bool:
    print("Checking for all software dependencies:")

    if check_platform():
        return check_openrazer() and check_colorchord() and check_sourcename()
    else:
        return False


def create_script(filename: str):
    absolute_path = os.path.abspath(".")
    script_str = ("#!/usr/bin/env bash\n"
                  "# enter the directory with colorchord\n"
                  "cd {}\n"
                  "# create the named pipe if it doesn't exist\n"
                  "test -e chroma_chord_pipe || mkfifo chroma_chord_pipe\n"
                  "# execute chroma_chord\n"
                  "./chroma_chord.py").format(absolute_path)

    with open(filename, "w") as script:
        script.writelines(script_str)
    os.chmod(filename, 0o754)
    print(filename, "created!")


if __name__=="__main__":
    if check_dependencies():
        print("All dependencies satisfied!")
        create_script("start_chroma_chord.sh")
