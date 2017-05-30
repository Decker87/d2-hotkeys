# Intro

d2-hotkeys is a keyboard macro program to help relieve pain caused by carpal tunnel and RSI when playing Diablo 2.

This program maps mouse clicks to keyboard keys to allow one to use hotkeys to cast D2 skills. For example, pressing the W key will cast the skill mapped to F5. This allows casting many skills without constantly hitting the F keys and right clicking. This is especially helpful for those with carpal tunnel syndrome or RSI, as mouse clicks can be very painful.

It works by doing exactly what players do - it quickly presses the F-keys and then right clicks to cast the skill.

# Installation (for non-programmers)

1. From the [releases](https://github.com/Decker87/d2-hotkeys/releases), download an install file
1. Run the install file, it will install by default to `C:\Program Files (x86)\d2Hotkeys`
1. From the start menu, run "d2Hotkeys" AS ADMINISTRATOR
1. To terminate the program, use the task manager. Look for "pythonw".

Note: I know it's inconvenient to terminate the program this way, but it only does its thing while D2 is in the foreground, so in practice you can just keep it running all the time.

# Installation (programmers)

1. Pull the source code
1. Install the external packages: `pythoncom` and `pyHook`
1. Open a terminal AS ADMINISTRATOR
1. Navigate to the base repo, and do: `python d2Hotkeys/main.py`

Note: This requires python 2.7.

# Using the program

1. The program will beep once to signal that it is running and listening for hotkeys.
1. The `~` key toggles the program on and off. A higher pitched beep means it's on.
1. Try toggling it a few times to see if you get higher and lower pitched beeps, then stop toggling after a high pitched beep.
1. Map teleport to F8.
1. With the program on, press R to teleport.
1. Note that the program will attempt to track how many times you press "Enter" so that you can still chat in game without casting skills. If you press Enter to do things like joining a game, it may get thrown off. To reset it just toggle with the `~` key.

By default, the mappings are:
- Q = left click
- W,E,R = F6,F7,F8 skills; right click
- A,S,D,F = F9,F10,F11,F12 skills; right click

Notes:
- These are configurable in d2-hotkeys-config.json (either in the install directory or in the repo you pulled).
- The program will only have an effect while D2 is in the foreground.

# FAQs

Q: Is this approved for private servers?

A: At the moment I have not sought approval from any private server hosts, so I would advise using it only for single player until it is approved.

Q: Nothing seems to be happening, why?

A: Check that the python process is running. If it isn't, double-check you are running as admin.

Q: It's running but the hotkeys are not working.

A: Try toggling it on and off with the `~` key. You may need to do this after pressing "Enter" in a game menu. The problem is the program doesn't know the difference between Enter used to start a chat or used some other way.

Q: It's not working, how can I get help?

A: Message me on reddit.
