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
import threading


class StoppableThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, daemon=True):
        self._request_stop = False
        super(StoppableThread, self).__init__(group=group,
                                              target=target,
                                              name=name,
                                              args=args,
                                              kwargs=kwargs,
                                              daemon=daemon)

    def run(self):
        while not self._request_stop:
            if self._target:
                self._target(*self._args, **self._kwargs)
            else:
                return

    def stop(self):
        self._request_stop = True
