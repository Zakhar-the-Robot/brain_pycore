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
from collections import deque
from typing import Any, Callable, List, Union
import zmq

from ..logging import LOG_LEVEL
from .base import ZmqBaseThread


class ZmqSubscriberThread(ZmqBaseThread):
    def __init__(self,
                 port: Union[int, List[int]],
                 topic: str,
                 callback: Callable[[str], None] = None,
                 address: str = "localhost",
                 thread_name="ZmqSubscriberThread") -> None:

        super().__init__(port=port, thread_name=thread_name)

        self.address = address
        self.topic = topic
        self.callback = callback
        self.socket = zmq.Context().socket(zmq.SUB)

    def start(self, log_level: LOG_LEVEL = LOG_LEVEL.INFO):
        self.socket.connect(f"tcp://{self.address}:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
        super().start(log_level)

    def _thread_target_once(self):
        data = self.socket_recv()
        topic = data[:len(self.topic)]
        messagedata = data[len(self.topic) + 1:]
        self.log.info(f"Received ({topic}): {messagedata}")
        if self.callback:
            self.callback(messagedata)
