"""IFR 1200 memory class and helpers
"""

# Global imports


# Local imports
import src.lib.helper
src.lib.helper.clear_debug_window()
from src.lib.helper import debug
from src.serialio import IFR1200Io
from src.display import IFR1200Display

io = IFR1200Io()        # create an instance of the IO class
disp = IFR1200Display()


# -------------------------------------------------------------------
def is_valid_frequency(freq) -> bool:
    """Check if the given frequency is valid
    :param freq: Frequency to test. Can be an integer, float or string

    >>> is_valid_frequency('a')
    False

    >>> is_valid_frequency(0)
    True

    >>> is_valid_frequency(1000.1)
    False
    """

    f = float(freq)
    if f < 0.0 or f >= 1000.0:
        print(f'Invalid frequency {freq}')
        return False

    return True


class IFR1200Memory:
    """IFR 1200 memory class"""

    # -------------------------------------------------------------------
    def __init__(self):
        """Intialize this class"""

        self.memory_bank = {}

        # Intialize the memory locatons with an empty frequency
        # for n in range(0, 16):
        #     self.memory_bank[n] = None

    # -------------------------------------------------------------------
    def set(self, n, x):
        """ Set memory location m to the given frequency x
            If no frequency is given, read the current frequency, and return it

        :param n: The memory location (0..15) to program
        :param x: A string, representing the frequency, "000.0000" to "999.9999"
        :return: the response
        """

        if not self.is_valid_memory_location(n):
            return ''

        if not is_valid_frequency(x):
            return ''

        # Set internal memory
        self.memory_bank[n] = x

        cmd = f"RFF{n}={x}\n"
        response = io.send_command(cmd)
        return response

    # -------------------------------------------------------------------
    def get(self, n):
        """Get the frequency from the given memory location"""

        if not self.is_valid_memory_location(n):
            return ''

        print(self.memory_bank.get(n, "undefined"))

        cmd = f"RFF{n}?\n"
        response = io.send_command(cmd)
        return response

    # -------------------------------------------------------------------
    def use(self, n):
        """ Execute RF specified by memory location n

        :param n: The memory location (0..15) to program
        :return: the response
        """

        if not self.is_valid_memory_location(n):
            return ''

        cmd = f"RFF{n}\n"
        response = io.send_command(cmd)
        return response

    # -------------------------------------------------------------------
    def set_and_use(self, n, x):
        """Set a memory location to the given frequency and use it"""

        if not self.is_valid_memory_location(n):
            return ''

        if not is_valid_frequency(x):
            return ''

    # -------------------------------------------------------------------
    @staticmethod
    def is_valid_memory_location(n: int) -> bool:
        """Check if the given memory location is valid
        :param n: The memory location to check (should be between 0 an 15
        :return: True if valid, False if not
        """

        if n < 0 or n > 15:
            print(f'Error, invalid memory location {n}')
            return False

        return True


# -------------------------------------------------------------------
if __name__ == "__main__":
    """The main of this module will perform some tests"""

    # src.lib.helper.clear_debug_window()
    debug(f"Testing {__file__}")

    # import doctest
    # doctest.testmod()

    mem = IFR1200Memory()

    mem.set(0, 96.80)
    disp.set("3FM")
    mem.set(1, 90.40)   # Arrow Jazz FM
    mem.set(2, 99.90)   # BNR Nieuws Radio
    mem.set(4, 1.800)   # Groot Nieuws Radio
    mem.set(5, 100.70)  # Q Music
    mem.set(6, 98.90)   # Radio 1
    mem.set(7, 92.60)   # Radio 2
    mem.set(8, 102.30)  # Radio 538
    disp.set("Radio 538")

    for loc in range(0, 6):
        print(mem.get(loc))

