import pythoncom
import pyHook
import Queue
import threading
import collections

# Pause and enable/disable are two different concepts
class Hooker:
    tKeyHookBehavior = collections.namedtuple("tKeyHookBehavior", ["keycode", "passThrough", "ignorePause"])
    tKeyEvent = collections.namedtuple("tKeyEvent", ["keycode", "timestamp", "isDownEvent"])

    def __init__(self, keyHookBehaviors, windowName = "", queueSize = 100):
        self.windowName = windowName
        self.pumpThread = None
        self.isPaused = False
        self.keysDown = set()

        # For hook behaviors, convert to a dict with a set for fast lookup
        self.keyHookBehaviors = {}
        for keyHookBehavior in keyHookBehaviors:
            self.keyHookBehaviors[keyHookBehavior.keycode] = keyHookBehavior
        self.keysHooked = set(self.keyHookBehaviors.keys())

        self.eventQueue = Queue.Queue(maxsize = queueSize)

    def start(self):
        if self.pumpThread:
            print "Hooking already started!"
            return False

        # Start it
        self.pumpThread = threading.Thread(target = self.pumpMessages)
        self.pumpThread.daemon = True
        self.pumpThread.start()

    def pumpMessages(self):
        # We must have the hooks in the same thread as the pump
        hm = pyHook.HookManager()
        hm.KeyDown = self.onKeyboardEvent
        hm.KeyUp = self.onKeyboardEvent
        hm.HookKeyboard()
        pythoncom.PumpMessages()

    def onKeyboardEvent(self, event):
        #print "KeyId: %i, Alt: %i, Extended: %i, Injected: %i, Message: %i, MessageName: '%s', Transition: %i" % (event.KeyID, event.Alt, event.Extended, event.Injected, event.Message, event.MessageName, event.Transition)

        # If it's an injected key event, don't process - this helps avoid infinite loops with automated keypresses
        if event.Injected:
            return True

        # If we're not in the right window, pass through
        if self.windowName != "" and event.WindowName != self.windowName:
            return True

        # If the key isn't in our list of ones we care about, pass through
        if event.KeyID not in self.keysHooked:
            return True

        # OK, it's a real event we care about
        keycode = event.KeyID
        timestamp = event.Time
        isDownEvent = (event.Message == 256 or event.Message == 260)    # key down, key sys down (when ALT is held)
        keyEvent = self.tKeyEvent(keycode, timestamp, isDownEvent)

        # If we're paused, pass through unless the behavior specifies otherwise
        if self.isPaused and not self.keyHookBehaviors[keycode].ignorePause:
            return True

        # Add it to the queue, if it isn't already down
        if isDownEvent and keycode in self.keysDown:
            # print "Key %i is already down, not adding to queue." % (keycode)
            pass
        elif not isDownEvent and keycode not in self.keysDown:
            # print "Key %i is already up, not adding to queue." % (keycode)
            pass
        else:
            # print "Adding to eventQueue: %s" % (keyEvent.__str__())
            self.eventQueue.put(keyEvent, block = False)
            if isDownEvent:
                self.keysDown.add(keycode)
            else:
                self.keysDown.discard(keycode)
        return self.keyHookBehaviors[keycode].passThrough

    def pause(self):
        self.isPaused = True

    def unpause(self):
        self.isPaused = False

if __name__ == '__main__':
    h = Hooker([Hooker.tKeyHookBehavior(0x41, True, False)])
    h.start()
    print h
    import time
    time.sleep(10)
    import presskeys
    presskeys.pressKey(0x41)
    time.sleep(10)
    presskeys.releaseKey(0x41)
    time.sleep(10)