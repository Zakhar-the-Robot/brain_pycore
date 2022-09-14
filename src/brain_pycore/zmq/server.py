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
from typing import Callable
import zmq
from .base import ZmqBaseThread


class ZmqServerThread(ZmqBaseThread):
    def __init__(self,
                 port: int,
                 callback: Callable[[str], str],
                 thread_name="ZmqServerThread") -> None:

        super().__init__(port=port, thread_name=thread_name)

        self.socket = zmq.Context().socket(zmq.REP)
        self.socket.bind(f"tcp://*:{self.port}")

        self.callback = callback

    def _thread_target_once(self):
        # Wait for next request from client
        request = self.socket_recv()
        self.log.info(f"Received: {request}")

        # Response
        response = self.callback(request)
        try:
            self.socket.send_string(response)
        except zmq.error.ZMQError:  # for thread termination
            return
        self.log.info(f"Response: {response}")
