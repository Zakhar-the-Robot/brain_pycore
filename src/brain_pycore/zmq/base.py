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
import zmq
from ..logging import new_logger, LOG_LEVEL
from ..thread import StoppableThread


class ZmqBaseThread():
    def __init__(self,
                 port: int,
                 thread_name="ZmqPublisherThread") -> None:

        self.thread_name = thread_name
        self.log = new_logger(self.thread_name)
        self.port = port
        self.socket = None
        self.thread = None  # type: None | StoppableThread

    def _thread_target_once(self):
        raise NotImplementedError

    def start(self, log_level: LOG_LEVEL = LOG_LEVEL.INFO):
        self.log.setLevel(log_level)
        self.thread = StoppableThread(target=self._thread_target_once,
                                      name=self.thread_name)
        self.thread.start()

    def stop(self):
        self.socket.close()
        self.thread.stop()
        while self.thread.is_alive():
            pass

    def socket_recv(self) -> str:
        data = None
        while not data:
            if self.thread.is_stopping:
                return ""
            try:
                data = self.socket.recv(flags=zmq.NOBLOCK)
            except zmq.Again as e:
                sleep(.1)
        return data.decode('ascii')

    @property
    def is_alive(self) -> bool:
        if self.thread:
            return self.thread.is_alive()
        else:
            return False
