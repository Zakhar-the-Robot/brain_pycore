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
from typing import Dict, Union
import can

from ..thread import StoppableThread


class CanBus:
    def __init__(self):
        self._started = False
        self._dev_can = can.interface.Bus(channel='can0', bustype='socketcan')
        self._thread = None  # type: Union[StoppableThread, None]
        self._device_log = {}  # type: Dict[int,datetime]
        self._messages = None  # type: Union[deque, None]

    def _canbus_listener(self):
        # print("CAN Listener start")
        while True:
            msg = self._dev_can.recv()  # type: Union[can.Message, None]
            if msg:
                id = (msg.arbitration_id >> 8) & 0xF
                now = datetime.now()
                # print(f"[Can Message] Time: {now}, Id: {hex(id)}")
                if id:
                    self._device_log[id] = now
                if self._messages is None:
                    raise RuntimeError  # inticates that there was some logical mistake earliear.
                    # This should not happen.
                self._messages.append(msg)

    @property
    def is_stopped(self):
        return not self._started

    @property
    def is_started(self):
        return self._started

    def start(self, max_messages: int = 0):
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
            if self._thread:
                self._thread.stop()
            self._thread = None
            self._started = False

    def get_last_device_log_time(self, device_id: int):
        return self._device_log.get(device_id)

    def get(self):
        """Get the last message"""
        if self._messages:
            return self._messages.pop()
        else:
            return None

    def send(self):
        """Send a message"""
        # TODO
        if self.is_started:
            pass


canbus = CanBus()
