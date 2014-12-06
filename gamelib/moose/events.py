#! /usr/bin/env python
'''
Events and Event Manager
'''
import pygame
import pygame.locals as pl

# This global is used by the clock controller
TICK_EVENT_TYPE = pl.USEREVENT + 1


def isUserEvent(event, name):
    ''' Returns True or False if the name matches the given event '''
    if event.type == pl.USEREVENT and event.number == CUSTOM_EVENTS[name]:
        return True
    else:
        return False


# All of these are classified as USEREVENT in pygame's terminology, so we
# use the numbers here to disambiguate them.
CUSTOM_EVENTS = {
    "Tick": 0,
    "FlipDebugDisplay": 1,
    "OneSecondEvent": 3,
    "PlaceEntity": 4,
    "MoveEntity": 5,
    "AddToForeground": 6,
    "EntityCreated": 7,
    "EntityMoved": 8,
    "MapCreated": 9,
    "ViewCreated": 10,
    "PlayerCreated": 11,
    "AddToBackground": 12,
    "RequestViewChangeTarget": 13
}


# This is kind of a hacky way to extend events, but I can't subclass them.
# Returns a function that, when called, creates an event with associated
# userdata.  The event name and number are already pre-filled with the data
# in CUSTOM_EVENTS, and the event type is always USEREVENT
def _makeEvent(name, number):
    def event_maker(userData=None, **kwargs):
        return pygame.event.Event(
            pl.USEREVENT, name=name, number=number,
            userData=userData, **kwargs)
    return event_maker
for k, v in CUSTOM_EVENTS.items():
    globals()[k] = _makeEvent(k, v)   # Adds all CUSTOM_EVENTS to the library's namespace


class EventManager(object):
    """
    An extension of pygame's event handler. This object is responsible for
    coordinating most communication between the Models, Views, and Controllers.

    Register any object with it by calling RegisterListener(), and that object
    will receive a callback on its notify() method whenever an event is fired.

    USAGE:

        REGISTERING AS A LISTENER USING CONSTRUCTOR
        import events

        class MyObject(object):
            def __init__(self, event_manager):
                self.evManager = event_manager   # often useful to keep a local reference
                self.evManager.RegisterListener(self)

            def notify(self, event):
                print event

        evManager = events.EventManager()
        myObject = MyObject(evManager)   # On any event, MyObject.notify() will
                                         # now be called.

        CREATING NEW EVENTS
        # Create the event by adding it to events.CUSTOM_EVENTS
        # In this example we assume CUSTOM_EVENTS has the following entry:
            ...
            "MyEvent": 1,
            ...

        SENDING EVENTS
        import events
        ev = events.MyEvent("Data to send")
        self.evManager.Post(ev)

        PROCESSING EVENTS
        while True:
            for event in pygame.event.get():
                evManager.notifyAllListeners(event)

        RECEIVING EVENTS
        import events

        ...  (inside the object's definition)
            def notify(self, event):
                if events.isUserEvent(event, "MyEvent"):
                print event.userData
        ...
        >>> "Data to send"
    """
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue = []

    def RegisterListener(self, listener):
        print "Registering {}".format(listener)
        self.listeners[listener] = 1

    def UnregisterListener(self, listener):
        if listener in self.listeners:
            del self.listeners[listener]

    def Post(self, event):
        ''' A thin wrapper around pygame's event post '''
        pygame.event.post(event)

    def notifyAllListeners(self, event):
        items = list(self.listeners.keyrefs())
        for listener in items:
            if event.type == TICK_EVENT_TYPE:
                print items
                print "NOTIFY {}".format(listener)
            listener.notify(event)
