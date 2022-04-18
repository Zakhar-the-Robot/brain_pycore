#!/usr/bin/env python3
# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************
from datetime import datetime
from collections import deque
from typing import Dict
import can

from brain_pycore.thread import StoppableThread


class CanBus:
    def __init__(self):
        self._dev_can = can.interface.Bus(channel='can0', bustype='socketcan_native')
        self._thread = None  # type: StoppableThread | None
        self._device_log = {}  # type: Dict[int,datetime]
        self._messages = None  # type: deque | None

    def _canbus_listener(self):
        # print("CAN Listener start")
        while True:
            msg = self._dev_can.recv()  # type: can.Message | None
            if msg:
                id = (msg.arbitration_id >> 8) & 0xF
                now = datetime.now()
                # print(f"[Can Message] Time: {now}, Id: {hex(id)}")
                if id:
                    self._device_log[id] = now
                self._messages.append(msg)

    def start(self, max_messages = None):
        if max_messages:
            self._messages = deque(maxlen = max_messages)
        else:
            self._messages = deque()
        self._thread = StoppableThread(target=self._canbus_listener)
        self._thread.start()

    def stop(self):
        self._thread.stop()
        self._thread = None
        self._messages = None
        
    def get(self):
        return self._messages.pop()
        
    def send(self):
        # TODO
        pass

canbus = CanBus()
