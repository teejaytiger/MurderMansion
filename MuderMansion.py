from _actions import action
from enum import Enum
class MuderMansion:
    """Main entry point for the game. It's basically a glorified state machine."""

    def __init__(self):
        self.act = action()

    def statem(self):
        pass


class STATES(Enum):
    TITLE = 0
    