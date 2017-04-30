from injectinput import pressKey, releaseKey, tapKey, pressMouseButton, releaseMouseButton, tapMouseButton
from hooks import Hooker
from keycodes import keyCodes
from time import sleep
from winsound import Beep
from collections import namedtuple

QuickKeyMapping = namedtuple('QuickKeyMapping', ['preKey', 'button'])

# Settings
pauseKey = keyCodes["`"]
chatKey = keyCodes["ENTER"]
quickKeyMappings = {}
quickKeyMappings[keyCodes["Q"]] = QuickKeyMapping(None, "left")
quickKeyMappings[keyCodes["W"]] = QuickKeyMapping(keyCodes["F6"], "right")
quickKeyMappings[keyCodes["E"]] = QuickKeyMapping(keyCodes["F7"], "right")
quickKeyMappings[keyCodes["R"]] = QuickKeyMapping(keyCodes["F8"], "right")
quickKeyMappings[keyCodes["A"]] = QuickKeyMapping(keyCodes["F9"], "right")
quickKeyMappings[keyCodes["S"]] = QuickKeyMapping(keyCodes["F10"], "right")
quickKeyMappings[keyCodes["D"]] = QuickKeyMapping(keyCodes["F11"], "right")
quickKeyMappings[keyCodes["F"]] = QuickKeyMapping(keyCodes["F12"], "right")

# Have to keep track of each button to know whether to push it down or not
buttonDownCounts = {"left": 0, "right": 0}

# States for managing hooking behavior
isInGame = False
isInChat = False

# Helpers
def goodBeep():
    Beep(1000, 250)

def badBeep():
    Beep(500, 250)

def beepGameState():
    if isInGame:
        goodBeep()
    else:
        badBeep()

# Main logic
def processHookedEvents(hooker):
    global isInGame, isInChat

    while True:
        keyEvent = hooker.eventQueue.get()
        print keyEvent

        # First see if it was the special key to enable / disable hooking
        if keyEvent.keycode == pauseKey:
            if keyEvent.isDownEvent:
                isInGame = not isInGame
                beepGameState()
                if isInGame:
                    isInChat = False
                    hooker.unpause()
                else:
                    hooker.pause()
            continue

        # Next see if it's the enter key, and if it is, manage chat state
        if keyEvent.keycode == chatKey:
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
                print "Tapping key 0x%02x" % (quickKeyMapping.preKey)
                #tapKey(quickKeyMapping.preKey, delayMid = 0.02, delayAfter = 0.02)
            if buttonDownCounts[quickKeyMapping.button] == 0:
                print "Pressing mouse button: %s" % (quickKeyMapping.button)
                #pressMouseButton(quickKeyMapping.button, delay = 0)
            buttonDownCounts[quickKeyMapping.button] += 1

        # Key up event
        else:
            # If we get a key up without keydown, don't go negative
            if buttonDownCounts[quickKeyMapping.button] > 0:
                buttonDownCounts[quickKeyMapping.button] -= 1
            if buttonDownCounts[quickKeyMapping.button] == 0:
                print "Releasing mouse button: %s" % (quickKeyMapping.button)
                #releaseMouseButton(quickKeyMapping.button, delay = 0)

def startHooking():
    global quickKeyMappings

    # Generate a list of key behaviors
    keyHookBehaviors = []
    
    # Pause and message are two special cases
    keyHookBehaviors.append(Hooker.tKeyHookBehavior(keycode = pauseKey, passThrough = False, ignorePause = True))
    keyHookBehaviors.append(Hooker.tKeyHookBehavior(keycode = chatKey, passThrough = True, ignorePause = False))

    # Add hooks from quick keys
    for keycode in quickKeyMappings:
        keyHookBehaviors.append(Hooker.tKeyHookBehavior(keycode = keycode, passThrough = False, ignorePause = False))

    # Start it up scotty
    hooker = Hooker(keyHookBehaviors)
    hooker.start()

    return hooker

if __name__ == "__main__":
    sleep(1)
    goodBeep()

    hooker = startHooking()
    processHookedEvents(hooker)