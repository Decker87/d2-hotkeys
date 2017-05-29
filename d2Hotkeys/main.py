from injectinput import tapKey, pressMouseButton, releaseMouseButton
from hooks import Hooker
from keycodes import keyCodes
from time import sleep
from winsound import Beep
from collections import namedtuple
import json, sys, os, inspect

# Helpers
def goodBeep():
    Beep(1000, 250)

def badBeep():
    Beep(500, 250)

# Beeps a good beep if value is truthy, else bad beep
def beepTrueOrFalse(value):
    if value:
        goodBeep()
    else:
        badBeep()

# Main logic
def processHookedEvents(hooker, keyConfig):
    # State tracking
    isInGame = False
    isInChat = False
    buttonDownCounts = {"left": 0, "right": 0}  # Track each button to know whether to push it down or not

    quickKeyMappings = keyConfig["quickKeys"]

    while True:
        try:
            keyEvent = hooker.eventQueue.get()

            # First see if it was the special key to enable / disable hooking
            if keyEvent.keycode == keyConfig["pauseKey"]:
                if keyEvent.isDownEvent:
                    isInGame = not isInGame
                    beepTrueOrFalse(isInGame)
                    if isInGame:
                        isInChat = False
                        hooker.unpause()
                    else:
                        hooker.pause()
                continue

            # Next see if it's the enter key, and if it is, manage chat state
            if keyEvent.keycode == keyConfig["chatKey"]:
                if keyEvent.isDownEvent and isInGame:
                    isInChat = not isInChat
                    if isInChat:
                        hooker.pause()
                    else:
                        hooker.unpause()
                continue

            # Now it must be one of the quick keys. Find the mapping in dict and do what we need to.
            quickKeyMapping = quickKeyMappings[keyEvent.keycode]

            # Key down event
            if keyEvent.isDownEvent:
                if quickKeyMapping.preKey:
                    tapKey(quickKeyMapping.preKey, delayMid = 0.02, delayAfter = 0.02)
                if buttonDownCounts[quickKeyMapping.button] == 0:
                    pressMouseButton(quickKeyMapping.button, delay = 0)
                buttonDownCounts[quickKeyMapping.button] += 1

            # Key up event
            else:
                # If we get a key up without keydown, don't go negative
                if buttonDownCounts[quickKeyMapping.button] > 0:
                    buttonDownCounts[quickKeyMapping.button] -= 1
                if buttonDownCounts[quickKeyMapping.button] == 0:
                    releaseMouseButton(quickKeyMapping.button, delay = 0)
        except:
            badBeep()
            print "ERROR: %s" % (sys.exc_info()[0])

def getConfig():
    # Try current working directory
    try:
        config = json.load(open("d2-hotkeys-config.json"))
        print "Found config in CWD"
        return config
    except:
        pass

    # Try 2 directories up from this file's location
    try:
        configPath = os.path.dirname(os.path.abspath(inspect.stack()[0][1])) + "%s..%s..%sd2-hotkeys-config.json" % (os.sep, os.sep, os.sep)
        config = json.load(open(configPath))
        print "Found config 2 dirs up from file"
        return config
    except:
        pass

def runFromJsonConfig():
    config = getConfig()

    # Generate a list of key behaviors
    tQuickKeyMapping = namedtuple('tQuickKeyMapping', ['preKey', 'button'])
    keyHookBehaviors = []
    keyConfig = {}
    
    # Pause and message are two special cases
    keyConfig["pauseKey"] = keyCodes[config["pauseKey"]]
    keyConfig["chatKey"] = keyCodes[config["chatKey"]]
    keyHookBehaviors.append(Hooker.tKeyHookBehavior(keycode = keyConfig["pauseKey"], passThrough = False, ignorePause = True))
    keyHookBehaviors.append(Hooker.tKeyHookBehavior(keycode = keyConfig["chatKey"], passThrough = True, ignorePause = True))

    # Quick keys
    keyConfig["quickKeys"] = {}
    for quickKeyEntry in config["quickKeys"]:
        keycode = keyCodes[quickKeyEntry["hookedKey"]]
        preKey = keyCodes[quickKeyEntry["preKey"]] if quickKeyEntry["preKey"] else None
        button = quickKeyEntry["button"]
        keyConfig["quickKeys"][keycode] = tQuickKeyMapping(preKey, button)
        keyHookBehaviors.append(Hooker.tKeyHookBehavior(keycode = keycode, passThrough = False, ignorePause = False))

    # Start it up scotty
    hooker = Hooker(keyHookBehaviors, "Diablo II")
    hooker.start()
    hooker.pause()
    badBeep()
    processHookedEvents(hooker, keyConfig)

def main():
    hooker = startHooking()
    processHookedEvents(hooker)

if __name__ == "__main__":
    runFromJsonConfig()