"""IFR 1200 serial commands and tests
"""

# Global imports
import time
import serial

# Local imports
import src.lib.helper
from src.lib.helper import debug


# ============================================================================
class IFR1200Io:
    """Class representing the serial Interface to IFR 1200"""

    # -------------------------------------------------------------------
    def __init__(self):
        """Intialize class IfrInterface"""

        self.comport = 'COM1:'
        self.baudrate = 9600
        self.serialport = None

        debug('Intializing serial port')

        try:
            self.serialport = serial.Serial(self.comport, baudrate=self.baudrate, timeout=0.2)
            debug('serial port is opened')
        except Exception as e:
            debug(f"EXCEPTION: {e}")
            self.serialport = None
            return

        self.send_lf()
        ret = self.ask_uok()
        if ret == b'%':
            debug(f"IFR1200Io is initialized")
        else:
            print('Error in initializing class IFR1200Io')

    # -------------------------------------------------------------------
    def send_command(self, cmd) -> bytes:
        """Send the given command to the IFR 1200 and wait for the response
        :param cmd: The string with the command to send
        :returns: The response (if any)
        """

        if not self.serialport:
            raise serial.SerialException

        bytes_waiting = self.serialport.inWaiting()
        if bytes_waiting:
            debug(f"UNEXPECTED: Still {bytes_waiting} bytes waiting in serial port before sending command {cmd}")
            s = self.serialport.read(bytes_waiting)
            debug(f"RESPONSE1 = {s}")

        if isinstance(cmd, bytes):
            pass
        elif isinstance(cmd, str):
            cmd = cmd.encode('utf-8')

        debug(f"Command: {cmd}")
        self.serialport.write(cmd)
        self.serialport.flush()
        time.sleep(0.2)

        # Only get response in the following cases:
        if b"?" in cmd or b'DUMP' in cmd or b'MTR1' in cmd or b'MTR2' in cmd or b'DTME' in cmd:
            ret = self.get_response(cmd)
            return ret

        bytes_waiting = self.serialport.inWaiting()
        if bytes_waiting:
            debug(f"UNEXPECTED: Still {bytes_waiting} bytes waiting in serial port after sending cmd {cmd}")
            s = self.serialport.read(bytes_waiting)
            debug(f"RESPONSE2 = {s}")
            return s

    # -------------------------------------------------------------------
    def get_response(self, cmd='') -> bytes:
        """ Wait for a response from the IFR.

        :param cmd: The command to send
        :returns: The stripped response
        """

        if not self.serialport:
            raise serial.SerialException

        # Determine the number of waiting, incoming bytes
        # debug(f"waiting for response for command [{cmd}]")
        time.sleep(0.2)  # Wait somewhat more time.
        bytes_waiting = self.serialport.inWaiting()
        # debug(f'bytes waiting = {bytes_waiting}')

        # Read the bytes, and append them to the return string
        s = self.serialport.read(bytes_waiting)
        debug(f"Response: {s}")

        if s.startswith(b"**"):
            print(f"ERROR: INVALID COMMAND [{cmd.decode().strip()}]")

        return s.strip()

    # -------------------------------------------------------------------
    def send_lf(self) -> str:
        """Send a single linefeed
        The 1200 should say on its display: RS-232 ENABLED

        :return: response of this command
        """

        cmd = b"\n\n"
        ret = self.send_command(cmd)
        return ret

    # -------------------------------------------------------------------
    def ask_uok(self):
        """ Check if the IFR can be reached and responds

        :returns: The response, which should be b'%\r\n'
        """

        cmd = b"UOK?\n"
        response = self.send_command(cmd)
        return response

    # -------------------------------------------------------------------
    def close(self):
        """Close the serial port"""

        self.serialport.close()


# -------------------------------------------------------------------
if __name__ == "__main__":
    """The main of this module will perform some tests"""

    # src.lib.helper.clear_debug_window()
    debug(f"Testing {__file__}")

    io = IFR1200Io()
    io.close()
