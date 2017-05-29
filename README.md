# Intro

This is keyboard & mouse macro program to allow one to use hotkeys to cast D2 skills. For example, pressing the W key will cast the skill mapped to F5. This allows casting many skills without constantly hitting the F keys and right clicking. This is especially helpful for those with carpal tunnel syndrome or RSI, as mouse clicks can be very painful.

It works by doing exactly what players do - it quickly presses the F-keys and then right clicks to cast the skill.

# Installation (for non-programmers)

1. From the [releases](https://github.com/Decker87/d2-hotkeys/releases), download an install file
1. Run the install file, it will install by default to `C:\Program Files (x86)\d2Hotkeys`
1. From the start menu, run "d2Hotkeys" AS ADMINISTRATOR
1. To terminate the program, use the task manager. Look for "pythonw".

# Installation (programmers)

1. Pull the source code
1. Install the external packages: `pythoncom` and `pyHook`
1. Open a terminal AS ADMINISTRATOR
1. Navigate to the base repo, and do: `python d2Hotkeys/main.py`

Note: This requires python 2.7.

# Using the program

1. The program will beep once to signal that it is running and listening for hotkeys.
1. The `~` key toggles the program on and off. A higher pitched beep means it's on.
1. Map teleport to F8.
1. With the program on, press R to teleport.
1. Note that the program will attempt to track how many times you press "Enter" so that you can still chat in game without casting skills. If you press Enter to do things like joining a game, it may get thrown off. To reset it just toggle with the `~` key.

By default, the mappings are:
- Q = left click
- W,E,R = F6,F7,F8 skills; right click
- A,S,D,F = F9,F10,F11,F12 skills; right click

These are configurable in config.json (either in the install directory or in the repo you pulled).
