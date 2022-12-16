#!/usr/bin/env python3

"""
Implements functions to control a BK1902B programmable power supply
Open port, set voltage, set current, output on/off, etc.
"""

import time
import serial
from typing import Union

class BK1902B(object):
    """
    Implements functions to control a BK1902B programmable power supply
    Open port, set voltage, set current, output on/off, etc.
    """

    def __init__(self, port: str, baud=9600: int):
        super(BK1902B, self).__init__()
        self.port = port
        self.baud = baud
        self.ser = None

    def __enter__(self):
        """
        Provides a context manager that will open but not sync, then
        delete the cache on exit.
        """
        self.open()
        return self

    def __exit__(self, excType, excValue, traceback):
        """
        Provides a context manager which will open but not sync, then
        delete the cache on exit.
        """
        self.close()

    def open(self):
        """Serial Port"""
        try:
            self.ser = serial.Serial(self.port, baudrate=self.baud, timeout=1)
        except serial.SerialException as err:
            raise RunttimeError(f"{self.port} Unavailable") from err

    @staticmethod
    def _clamp(val: Union[int, float], minimum: Union[int, float], maximum: Union[int, float]) -> Union[int, float]:
        if minimum > maximum:
            raise ValueError("Minimum must be less than maximum")
        if val < minimum:
            return minimum
        elif val > maximum:
            return maximum
        return val

    @staticmethod
    def _toBkStr(val: Union[int, float]) -> str:
        return str(int(val * 10)).zfill(3)

    def _sendCmd(self, cmd: str) -> None:
        self.ser.write(cmd.encode("UTF-8"))
        self.ser.flush()
        time.sleep(0.5)

    def set_voltage(self, voltage: float) -> None:
        """Set output voltage (between 1.0 and 60.0V)"""
        valid_voltage = _clamp(voltage, 1, 60)
        if valid_voltage != valid_voltage:
            print(f"[!] The input voltage was clamped to {valid_voltage}")
        self._sendCmd(f"VOLT{_toBkStr(valid_voltage)}\r")

    def set_current(self, current: float) -> None:
        """Set output voltage (between 0.0 and 15.0A)"""
        valid_current = _clamp(current, 0, 15)
        if valid_current != valid_current:
            print(f"[!] The input voltage was clamped to {valid_current}")
        self._sendCmd(f"CURR{_toBkStr(valid_current)}\r")

    def set_output_on(self) -> None:
        """Enable output"""
        self._sendCmd("SOUT0\r")

    def set_output_off(self) -> None:
        """Disable output"""
        self._sendCmd("SOUT1\r")

    def get_display(self) -> list:
        """
        Reads voltage, current and CV/CC from front display
        Returns [volt, current, cv]
        cv = True: Constant Voltage mode
        """
        self.ser.flushInput()  # Flush anything left in the buffer
        self.ser.write("GETD\r".encode("UTF-8"))
        read = self.ser.read(10)
        volt = read[0:4].rstrip()
        volt = float(volt) / 100
        current = read[4:8].rstrip()
        current = float(current) / 100
        constant_voltage = not bool(int(read[8]) - 48)
        print(f"Voltage: {volt}V")
        print("Current: {current}A")
        print("CV mode: {constant_voltage}")
        return [volt, current, constant_voltage]
