class EventSourcer():

    def __init__(self):
        self.value = 0
        # event_history and redo_queue will hold all events. redo_queue will hold events removed from the history
        # because of undo(). Using lists because they can act like a stack with the way python implements pop().
        # Events will be represented by tuples of (value of event, addition or subtraction
        # (True or False, respectively)). redo_stack will be used as a queue instead of a stack.

        # Using 0's and 1's might be more memory intensive compared to making a number negative,
        # but in the end it shouldn't really matter because it's 1 extra bit of information. It's also more versatile
        # against edge cases than making a number negative (i.e. inputting a negative number).
        self.event_history = []
        self.redo_queue = []

    def add(self, num: int):
        self.value += num
        self.event_history.append((num, False))
        # Could be cleaner but one liners rule supreme
        self.redo_queue.pop() if len(self.redo_queue) != 0 else None

    def subtract(self, num: int):
        self.value -= num
        self.event_history.append((num, True))
        self.redo_queue.pop() if len(self.redo_queue) != 0 else None

    def undo(self):
        if len(self.event_history) > 0:
            last_event = self.event_history.pop()
            # Again, this could be cleaner but one liners rule supreme
            self.value = self.value + last_event[0] if last_event[1] else self.value - last_event[0]
            # Insert at the beginning of the list
            self.redo_queue.insert(0, last_event)

    def redo(self):
        if len(self.redo_queue) > 0:
            last_event = self.redo_queue.pop()
            self.value = self.value + last_event[0] if not last_event[1] else self.value - last_event[0]

    def bulk_undo(self, steps: int):
        for i in range(steps):
            if len(self.event_history) > 0:
                self.undo()

    def bulk_redo(self, steps: int):
        for i in range(steps):
            if len(self.redo_queue) > 0:
                self.redo()
