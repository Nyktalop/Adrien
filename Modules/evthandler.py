class EvtHandler:
    def __init__(self):
        self.current_keys = []
        self.key_pressed = []
        self.key_released = []
        self.subscribers = []

    def evt_key_pressed(self, evt):
        if not evt.keysym in self.key_pressed and not evt.keysym in self.current_keys:
            self.key_pressed.append(evt.keysym)
            self.current_keys.append(evt.keysym)

    def evt_key_released(self, evt):
        if evt.keysym in self.current_keys:
            self.key_released.append(evt.keysym)
            del (self.current_keys[self.current_keys.index(evt.keysym)])

    def add_subscriber(self, entity):
        if not entity in self.subscribers:
            self.subscribers.append(entity)

    def publish(self):

        for sub in self.subscribers:
            sub.next_step(self.key_pressed, self.key_released)

        self.key_pressed = []
        self.key_released = []