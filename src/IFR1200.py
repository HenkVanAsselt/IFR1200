"""IFR 1200 serial commands and tests
"""

import time
import serial

# import sys
# sys.path.append('lib')

import src.lib.helper
from src.lib.helper import debug


# class IFR1200Io:
#     """Interface to IFR 1200"""
#
#     # -------------------------------------------------------------------
#     def __init__(self):
#         """Intialize class IfrInterface"""
#
#         self.comport = 'COM1:'
#         self.baudrate = 9600
#         self.serialport = serial.Serial(self.comport, baudrate=self.baudrate, timeout=0.2)
#
#     # -------------------------------------------------------------------
#     def send_command(self, cmd) -> bytes:
#         """Send the given command to the IFR 1200 and wait for the response
#         :param cmd: The string with the command to send
#         :returns: The response (if any)
#         """
#
#         bytes_waiting = self.serialport.inWaiting()
#         if bytes_waiting:
#             debug(f"UNEXPECTED: Still {bytes_waiting} bytes waiting in serial port before sending command {cmd}")
#             s = self.serialport.read(bytes_waiting)
#             debug(f"RESPONSE1 = {s}")
#
#         if isinstance(cmd, bytes):
#             pass
#         elif isinstance(cmd, str):
#             cmd = cmd.encode('utf-8')
#
#         debug(f"Sending command [{cmd}]")
#         self.serialport.write(cmd)
#         self.serialport.flush()
#         time.sleep(0.2)
#
#         # Only get response in the following cases:
#         if b"?" in cmd or b'DUMP' in cmd or b'MTR1' in cmd or b'MTR2' in cmd or b'DTME' in cmd:
#             ret = self.get_response(cmd)
#             return ret
#
#         bytes_waiting = self.serialport.inWaiting()
#         if bytes_waiting:
#             debug(f"UNEXPECTED: Still {bytes_waiting} bytes waiting in serial port after sending cmd {cmd}")
#             s = self.serialport.read(bytes_waiting)
#             debug(f"RESPONSE2 = {s}")
#             return s
#
#     # -------------------------------------------------------------------
#     def get_response(self, cmd='') -> bytes:
#         """ Wait for a response from the IFR.
#
#         :param cmd: The command to send
#         :returns: The stripped response
#         """
#
#         debug(f"waiting for response for command [{cmd}]")
#
#         ret = b''
#
#         bytes_waiting = self.serialport.inWaiting()
#         debug(f'bytes waiting1 = {bytes_waiting}')
#         time.sleep(0.2)     # Wait somewhat more time.
#         bytes_waiting = self.serialport.inWaiting()
#         debug(f'bytes waiting2 = {bytes_waiting}')
#         s = self.serialport.read(bytes_waiting)
#         debug(f"response = [{s}]")
#         ret += s
#
#         if ret.startswith(b"**"):
#             print(f"ERROR: INVALID COMMAND [{cmd.decode().strip()}]")
#
#         return ret.strip()






# -------------------------------------------------------------------
def set_mode(self, mode='REC'):
    """ Set IFR in rmote mode (take control of the switches)

    'REM' = Remote Mode
    'REC' = Receive Mode
    'DUP' = Duplex Mode
    'DPG' = Duplex Generate Mode

    :param mode: String with the required mode
    """

    valid_modes = ['REM', 'REC', 'DUP', 'DPG']

    if mode not in valid_modes:
        print(f"ERROR: Invalid mode {mode}")
        return

    cmd = f"{mode}\n"
    response = self.send_command(cmd)
    return response


# -------------------------------------------------------------------
def get_frequencies(self):
    """Get the frequencies of all memory locations"""

    for n in range(0, 15):
        f = self.get_frequency(n)
        debug(f"{n}={f}")
        print(f"{n}={f}")

# -------------------------------------------------------------------
def set_modulation(self, m=''):
    """ Set specified modulation

    :param m: Modulation type to set
    :return: Current Modulation type
    """

    # Check if given memory location is valid
    if m not in ['AM1', 'AM2', 'SSB', 'FM1', 'FM2', 'FM3']:
        print(f"Error in given modulation setting {m}")
        return ''

    ret = self.send_command(m)
    return ret

# -------------------------------------------------------------------
def get_version(self) -> str:
    """ Get version string

    :return: the response
    """

    cmd = "VER?\n"
    response = self.send_command(cmd)
    return response

# -------------------------------------------------------------------
def close_serial(self):
    """Close the serial port"""
    self.serialport.close()

# -------------------------------------------------------------------
def scan(self, start_freq, end_freq, delta_freq, sleeptime):
    """Scan over the given frequency range"""

    # Scanner
    f = start_freq
    while f < end_freq:
        fstr = "%08.4f" % f
        print(fstr)
        ifr.set_and_use_frequency(x=fstr)
        ifr.get_frequency(0)
        time.sleep(sleeptime)
        f += delta_freq

    return ''

# -------------------------------------------------------------------
def set_freq_error_meter(self, x) -> str:
    """Set FREQ ERROR Meter to RF range as stored in x

    1 = 30 Hz RF
    2 = 100 Hz RF
    3 = 300 Hz RF
    4 = 1 kHz RF
    5 = 3 kHz RF
    6 = 10 kHz RF

    :param x: The mode to set to, see above
    """

    cmd = f"RFE{x}\n"

    if x not in [1, 2, 3, 4, 5, 6]:
        print(f"Invalid command {cmd}")
        return ''

    response = self.send_command(cmd)
    return response

# -------------------------------------------------------------------
def set_modulation_meter(self, x) -> str:
    """Set Modulation Meter as stored in x

    2 = 2 kHz or 20% full scale
    6 = 6 kHz or 60% full scale
    20 = 20 kHz or 200% Full scale
    60 = 60 kHz or 600% Full scale

    SIG = Measure relative signal strength
    DIS = Measure Distortion
    SID = Measure SINAD
    BAT = Measure internal battery voltage
    15A = 15 W Average Power range
    150A = 150 W Average Power range
    15P = 15 W Peak Power range
    150P = 150 W Peak Power range

    :param x: The mode to set to, see above

    """

    if isinstance(x, int):
        cmd = f"R{x}\n"
        response = self.send_command(cmd)
        return response

    elif x in ['DIS', 'SID', 'BAT', 'SIG', '15A', '150A', '15P', '150P']:
        cmd = x + '\n'
        response = self.send_command(cmd)
        return response

    else:
        print(f"INVALID modulation meter command {x}")
        return ''

# -------------------------------------------------------------------
def set_vfd_to_mtr2(self):
    """Set VDF (Vacuum Fluorescent Display) to meters and returns current value of modulation
    as stored in range and function selected
    """

    cmd = f"MTR2?\n"
    response = self.send_command(cmd)
    return response


# # --------------------------------------------------------------------
# def run_tests(serport):
#     """Run some tests
#
#     :param serport: Serial port
#     """
#
#     _s = show_text("PY Intializing")
#     _s = get_version()
#
#     _s = set_and_use_frequency(x="102.2000")
#     _s = set_and_use_frequency(x="099.2000")
#     _s = set_and_use_frequency(x="102.4000")
#
#     # # Scanner
#     # x = 90.0
#     # while x < 103.5:
#     #     x = x + 0.1
#     #     freq = "%08.4f" % x
#     #     print(freq)
#     #     _s = set_and_use_frequency(serport, x=freq)
#     #     _s = get_frequency(serport, 0)
#
#     _s = set_mem_frequency(n=0, x='102.0000')
#     _s = set_mem_frequency(n=1, x='102.1000')
#     _s = set_mem_frequency(n=2, x='102.2000')
#     _s = set_mem_frequency(n=3, x='102.3000')
#
#     _s = get_frequency( 0)
#     _s = get_frequency( 1)
#     _s = get_frequency( 2)
#     _s = get_frequency( 3)
#
#     use_mem_frequency( n=0)
#     use_mem_frequency( n=1)
#     use_mem_frequency( n=2)
#     use_mem_frequency( n=3)


# -------------------------------------------------------------------
if __name__ == "__main__":
    src.lib.helper.clear_debug_window()

    ifr = IfrInterface()

    _s = ifr.send_lf()
    _s = ifr.ask_uok()
    _s = ifr.get_version()

    _s = ifr.set_mode('REC')
    _s = ifr.set_and_use_frequency('144.8000')
    _s = ifr.set_modulation('FM3')

    # # Scanner
    # _s = ifr.scan(88.0, 106.0, 0.1, 1.0)
    # _s = ifr.set_and_use_frequency('144.8000')

    # _s = ifr.get_frequencies()

    # for x in range(1, 7):
    #     ifr.set_freq_error_meter(x)

    for n in [2, 6, 20, 60]:
        ifr.set_modulation_meter(n)

    for s in ['DIS', 'SID', 'BAT', 'SIG', '15A', '150A', '15P', '150P']:
        ifr.set_modulation_meter(s)

    _s = ifr.set_vfd_to_mtr2()
    _s = ifr.set_vfd_to_mtr2()

