# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************
from datetime import datetime
from collections import deque
from typing import Dict
import can

from ..thread import StoppableThread


class CanBus:
    def __init__(self):
        self._started = False
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
               
    @property
    def is_stopped(self):
        return not self._started
               
    @property
    def is_started(self):
        return self._started

    def start(self, max_messages=None):
        if self.is_stopped:
            if max_messages:
                self._messages = deque(maxlen=max_messages)
            else:
                self._messages = deque()
            self._thread = StoppableThread(target=self._canbus_listener)
            self._thread.start()
            self._started = True
        else:
            print("Already started")

    def stop(self):
        if self.is_started:
            self._thread.stop()
            self._thread = None
            self._started = False

    def get(self):
        if self._messages:
            return self._messages.pop()
        else:
            return None

    def send(self):
        # TODO
        if self.is_started:
            pass


canbus = CanBus()
