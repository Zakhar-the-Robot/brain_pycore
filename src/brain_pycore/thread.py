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
