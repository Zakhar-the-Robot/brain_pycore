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
from queue import Empty, Queue
import zmq

from brain_pycore.logging import LOG_LEVEL
from .base import ZmqBaseThread


class ZmqClientThread(ZmqBaseThread):
    def __init__(self,
                 port: int,
                 buffer_size=8,
                 address: str = "localhost",
                 thread_name="ZmqClientThread") -> None:

        super().__init__(port=port, thread_name=thread_name)

        self.address = address
        self.socket = zmq.Context().socket(zmq.REQ)
        self.requests = Queue(maxsize=buffer_size)
        self.responses = Queue(maxsize=1)

    def start(self, log_level: LOG_LEVEL = LOG_LEVEL.INFO):
        self.socket.connect(f"tcp://{self.address}:{self.port}")
        super().start(log_level)

    def send(self, req: str) -> str:
        self.requests.put(req)
        return self.responses.get()[1]

    def _thread_target_once(self):
        # Request
        try:
            req = self.requests.get(timeout=.1)
        except Empty:
            return
        self.socket.send_string(req)
        self.log.info(f"Sent: {req}")

        # Response
        resp = self.socket_recv()
        self.responses.put((req, resp))
        self.log.info(f"Response: {resp}")
