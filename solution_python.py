class EventSourcer():

    def __init__(self):
        self.value = 0
        # event_history and redo_stack will hold all events. redo_stack will hold events removed from the history
        # because of undo(). Using lists because they can act like a stack with the way python implements pop().
        # Events will be represented by tuples of (value of event, addition or subtraction
        # (True or False, respectively)).

        # Using 0's and 1's might be more memory intensive compared to making a number negative,
        # but in the end it shouldn't really matter because it's 1 extra bit of information. It's also more versatile
        # against edge cases than making a number negative (i.e. inputting a negative number).

        # Solution space complexity: O(N)
        self.event_history = []
        self.redo_stack = []

    # Runtime complexity: O(1)
    def add(self, num: int):
        self.value += num
        self.event_history.append((num, False))
        # Could be cleaner but one liners rule supreme
        self.redo_stack.pop() if len(self.redo_stack) != 0 else None

    # Runtime complexity: O(1)
    def subtract(self, num: int):
        self.value -= num
        self.event_history.append((num, True))
        self.redo_stack.pop() if len(self.redo_stack) != 0 else None

    # Runtime complexity: O(1)
    def undo(self):
        if len(self.event_history) > 0:
            last_event = self.event_history.pop()
            # Again, this could be cleaner but one liners rule supreme
            self.value = self.value + last_event[0] if last_event[1] else self.value - last_event[0]
            # Insert at the beginning of the list
            self.redo_stack.append(last_event)

    # Runtime complexity: O(1)
    def redo(self):
        if len(self.redo_stack) > 0:
            last_event = self.redo_stack.pop()
            self.value = self.value + last_event[0] if not last_event[1] else self.value - last_event[0]

    # Runtime complexity: O(N)
    def bulk_undo(self, steps: int):
        for i in range(steps):
            if len(self.event_history) > 0:
                self.undo()

    # Runtime complexity: O(N)
    def bulk_redo(self, steps: int):
        for i in range(steps):
            if len(self.redo_stack) > 0:
                self.redo()
            else:
                break
