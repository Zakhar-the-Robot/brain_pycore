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
from time import sleep
from typing import Callable
import zmq
from .base import ZmqBaseThread


class ZmqPublisherThread(ZmqBaseThread):
    def __init__(self,
                 port: int,
                 topic: str,
                 publish_callback: Callable[[], str],
                 thread_name="ZmqPublisherThread",
                 publishing_freq_hz: int = 1) -> None:

        super().__init__(port=port, thread_name=thread_name)

        self.topic = topic
        self.socket = zmq.Context().socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{self.port}")

        if publishing_freq_hz == 0:
            self.publishing_period_s = 0
        else:
            self.publishing_period_s = 1.0 / publishing_freq_hz
        self.publish_callback = publish_callback

    def _thread_target_once(self):
        data = self.publish_callback()
        to_send = f"{self.topic} {data}"
        self.socket.send_string(to_send)
        self.log.info(f"Published ({self.topic}): {data}")
        sleep(self.publishing_period_s)
