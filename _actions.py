"""
Speaking to someone
interacting with an object
analyzing a room
hiding something
performing a spell
wishing
"""

from _abstr import ACTION\
from _inventory import inventory, book
from _character import _character

class action:
    def __init__(self, character):
        self.me = character

    def read(self, book):
        pass

    def set_trap(self, trap):
        pass

    def cast(self, spell):
        pass

    def struggle(self):
        pass

    def use_tool(self, tool):
        pass

    def craft(self):
        pass
