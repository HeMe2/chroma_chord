# Chroma Chord

Computer audio to light conversion for Razer RGB keyboards on Linux.

This software is intended to run permanently in the background, so it can grab all the audio played by the computer. Then it uses [ColorChord](https://github.com/cnlohr/colorchord) to convert this audio to colorful voronoi diagrams, which are then displayed on the RGB keys of your Razer keyboard using the [OpenRazer](https://openrazer.github.io/) Python API. After three seconds of silence (eg. no light on the keyboard) the "starlight" effect is set on the keyboard. On quit, the same effect is set.

I created this as a quick draft two years ago. I wanted to beautify the code and the overall concept. But since it runs flawless on my machine every day, I never found the motivation to finally rework the code.
Now I decided to add some documentation and a handy dependency checker and start script creator and finally uplolad my butchered code.

Once I encountered problems with an onboard soundcard, but since I'm not using this, I didn't dig into it. It works very well with the two USB soundcards (interfaces) I've got. And it worked well on my laptops onboard soundcard.

## Important notice

The current ColorChord master doesn't run in headless mode, thus you need to use an [older commit](https://github.com/cnlohr/colorchord/commit/9a89be3aa8ae366df85ecb9f8cb611ad202a416e). I'm on it, to make it work soon.

## Dependencies

  - Linux
  - Python3
  - [OpenRazer](https://github.com/openrazer/openrazer#installation)
  - [ColorChord](https://github.com/cnlohr/colorchord)
    - clone project with: `git clone --recursive https://github.com/cnlohr/colorchord`
    - `cd colorchord/colorchord2`
    - `git checkout 9a89be3aa8ae366df85ecb9f8cb611ad202a416e` (Hopefully this step won't be needed in future)
    - `make`

## How to Chroma Chord

How to execute this hacky piece of software:
  1. Make sure you have OpenRazer installed and a binary of ColorChord.
  2. Copy the colorchord binary in the Chroma Chord folder.
  3. Set the `sourcename` of your soundcard in `chroma_chord_voronoi.conf`
     Use `pactl list | grep pci- | grep monitor` to get the name of your device. 
     Or just: ` pactl list | grep monitor ` if you're using an USB soundcard or something similar.
  4. Run `./create_start_script.py` (must be executed from the same folder)
     This checks whether all dependencies are satisfied and creates the `start_chroma_chord.sh`
  5. Finally start Chroma Chord with the `./start_chroma_chord.sh` (can be called from every folder)

If you like you can than add the `start_chroma_chord.sh` to the autostart of your system.


## To-Do:

  - add Licence
  - add header comments
  - create video demonstration
  - get rid of code TODOs
  - provide this functionality as a output device for colorchord