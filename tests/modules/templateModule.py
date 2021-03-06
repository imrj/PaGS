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
Template module - for testing only
"""
from PaGS.modulesupport.module import BaseModule


class Module(BaseModule):
    """
    small test module for the manager tests
    """
    def __init__(self, loop, txClbk, vehListClk, vehObjClk, cmdProcessClk, prntr, settingsDir, isGUI, loadGUI):
        BaseModule.__init__(self, loop, txClbk, vehListClk, vehObjClk, cmdProcessClk, prntr, settingsDir, isGUI, loadGUI)

        self.pkts = 0
        # self.vehRef = {}
        self.theVeh = []
        self.printedout = {}

        self.calledStuff = {}

        self.shortName = "template"
        self.commandDict = {'do_stuff': self.stuff, "crash": self.crash}

    def stuff(self, veh: str, arg: int, arrg: str):
        """a user command"""
        self.calledStuff[veh] = "" + str(arg) + "," + arrg

    def crash(self):
        """deliberately to something bad"""
        self.badvar += 1

    def printVeh(self, text: str, name: str):
        """
        Send any printed text to a dict
        """
        self.printedout[name] = text

    def addVehicle(self, name: str):
        self.theVeh.append(name)

    def incomingPacket(self, vehname: str, pkt):
        """
        Send a packet back out
        """
        self.pkts += 1
        # need a ref to the vehicle...
        self.txCallback(vehname, self.vehObj(vehname).mod.MAVLINK_MSG_ID_HEARTBEAT,
                        type=self.vehObj(vehname).mod.MAV_TYPE_GCS,
                        autopilot=self.vehObj(vehname).mod.MAV_AUTOPILOT_INVALID,
                        base_mode=0,
                        custom_mode=0,
                        system_status=0,
                        mavlink_version=int(self.vehObj(vehname).mavversion))

        # cause an exception:
        if pkt.base_mode == 1:
            self.crash()

    def removeVehicle(self, name: str):
        self.theVeh.remove(name)
