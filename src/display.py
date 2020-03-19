"""IFR 1200 display class
"""

# Local imports
from src.lib.helper import debug
from src.serialio import IFR1200Io

# create an instance of the IO classs
io = IFR1200Io()


# ============================================================================
class IFR1200Display:
    """Class representing the IFR 1200 display """

    # -------------------------------------------------------------------
    def __init__(self):
        """Intialize this class"""

        self.text = ''

    # -------------------------------------------------------------------
    def set(self, text) -> str:
        """Show the given text on the display
        :param text: The text to display
        """

        if not text:
            return ''

        # Save the text
        self.text = text

        # Program the IFR to show the text.
        cmd = f"!{text}\n".encode('utf-8')
        response = io.send_command(cmd)
        return response

    # -------------------------------------------------------------------
    def get(self) -> str:
        """Return the text which should be shown on the display

        >>> set("test1")
        >>> get()
        'something else'

        """

        return self.text


# -------------------------------------------------------------------
if __name__ == "__main__":
    """The main of this module will perform some tests"""

    # src.lib.helper.clear_debug_window()
    debug(f"Testing {__file__}")

    disp = IFR1200Display()

    disp.set('Hello Henk')
    print(disp.get())

    disp.set('Oh oh')
    print(disp.get())


