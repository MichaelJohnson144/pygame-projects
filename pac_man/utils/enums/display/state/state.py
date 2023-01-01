# |*************************************************************************************************************|
# |                          | "PRE-DEFINE" the Program's "'STATE MACHINE' CONSTANTS" |                         |
# |*************************************************************************************************************|
class State:
    def __init__(self):
        (
            # "'Pre-define' the '''main' menu's' 'states:''"
            self.START_GAME,
            self.OPTIONS,
            self.CREDITS,
            # "'Pre-define' the '''options' menu's' 'states:''"
            self.VOLUME,
            self.CONTROLS,
            self.GRAPHICS,
        ) = ("Start Game", "Options", "Credits", "Volume", "Controls", "Graphics")
