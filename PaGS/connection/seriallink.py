"""
The Python-async Ground Station (PaGS), a mavlink ground station for
autonomous vehicles.
Copyright (C) 2019  Stephen Dade

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

"""
Module for defining udp connections to mavlink
"""
import fnmatch
import serial.tools.list_ports

from PaGS.connection.mavconnection import MAVConnection


class SerialConnection(MAVConnection):
    """
    A MAVLink Serial port connection
    """
    def __init__(self, dialect: str, mavversion: float, name: str,
                 srcsystem: int, srccomp: int, rxcallback, clcallback=None) -> None:
        MAVConnection.__init__(self, dialect, mavversion, name,
                               srcsystem, srccomp, rxcallback, clcallback)
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        self.processPackets(data)

    def send_data(self, data: bytes) -> None:
        """Send data across the link"""
        if self.transport is not None:
            self.transport.write(data)

    def close(self):
        if self.transport:
            self.transport.close()


def findserial():
    """
    Return the port(s) that are likely to be a flight controller
    """
    ret_list = []
    serial_list = [
        '*FTDI*',
        "*Arduino_Mega_2560*",
        "*3D*",
        "*USB_to_UART*",
        '*Ardu*',
        '*PX4*',
        '*Hex_*',
        '*Holybro_*',
        '*mRo*',
        '*FMU*',
        '*Kakute*',
        '*Pixhawk*']

    ports = list(serial.tools.list_ports.comports())
    for port, description, hwid in ports:
        for preferred in serial_list:
            if (fnmatch.fnmatch(description.lower(), preferred.lower()) or
                    fnmatch.fnmatch(hwid.lower(), preferred.lower())):
                ret_list.append(port)
    return ret_list
