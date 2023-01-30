"""Globally available program state, where __main__.py and modules can share variables
Not thread safe!
"""

# Program dom root
root:object

# needs to be called absolute first in __main_.py before any modules are run
def init():
    # All loaded modules
    global modules
    modules = list[object]()
    global root
    root= None
