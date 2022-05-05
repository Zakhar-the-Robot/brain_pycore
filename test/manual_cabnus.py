#!/usr/bin/env python3
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
import brain_pycore


def wait(wait_sec=5):
    for i in range(wait_sec):
        sleep(1)
        print(f"Collecting messages: {i+1} sec...")


def report() -> int:
    msgs = brain_pycore.can.canbus._messages
    if msgs:
        print(f"Messages: {len(msgs)}")
    else:
        print(f"No messages!")

    print("Device log:")
    print(brain_pycore.can.canbus._device_log)
    if msgs:
        return len(msgs)
    else:
        return 0


if __name__ == "__main__":
    brain_pycore.can.canbus.start(30)

    for i in range(3):
        wait()
        brain_pycore.can.canbus.start()
        msg_num = report()
        msg = brain_pycore.can.canbus.get()
        assert msg is not None
        print(f"The last msg: {msg}")

        # Send amount of messages
        brain_pycore.can.canbus.send(0xaa, [
            msg_num & 0xff,
            msg_num >> 8 & 0xff,
            msg_num >> 16 & 0xff,
            msg_num >> 24 & 0xff,
            msg_num >> 32 & 0xff,
            msg_num >> 40 & 0xff,
            msg_num >> 48 & 0xff,
            msg_num >> 56 & 0xff,
        ])

    brain_pycore.can.canbus.stop()
    print("Stopped")
