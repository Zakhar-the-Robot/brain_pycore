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
import sys
from collections import deque
from time import sleep
from multiprocessing import Process, Queue
import subprocess

import can
import brain_pycore

def process_2(a,b):
    m = brain_pycore.can.canbus.get()
    if m:
        print(m)
    else:
        raise AssertionError("No message")


if __name__ == "__main__":
    brain_pycore.can.canbus._messages = deque(maxlen=5)
    
    
    msg1 = can.Message(
                arbitration_id=0x11, 
                data=[1,2,3,4,5,6,7,8], 
                is_extended_id=False
                )
    msg2 = can.Message(
                arbitration_id=0x22, 
                data=[1,2,3,4,5,6,7,8], 
                is_extended_id=False
                )
    brain_pycore.can.canbus._messages.append(msg1)
    brain_pycore.can.canbus._messages.append(msg2)
    
    exec_string = f"""{sys.executable} -c "import brain_pycore; m = brain_pycore.can.canbus.get(); print(m)" """
    subprocess = subprocess.Popen(exec_string, shell=True, stdout=subprocess.PIPE)
    subprocess_return = str(subprocess.stdout.read().decode('ascii'))
    print(subprocess_return)
    if "None" in subprocess_return:
        raise AssertionError("Cannot read the message")

    # for i in range(3):
    #     wait()
    #     brain_pycore.can.canbus.start()
    #     msg_num = report()
    #     msg = brain_pycore.can.canbus.get()
    #     assert msg is not None
    #     print(f"The last msg: {msg}")

    #     # Send amount of messages
    #     brain_pycore.can.canbus.send(0xaa, [
    #         msg_num & 0xff,
    #         msg_num >> 8 & 0xff,
    #         msg_num >> 16 & 0xff,
    #         msg_num >> 24 & 0xff,
    #         msg_num >> 32 & 0xff,
    #         msg_num >> 40 & 0xff,
    #         msg_num >> 48 & 0xff,
    #         msg_num >> 56 & 0xff,
    #     ])

    # brain_pycore.can.canbus.stop()
    # print("Stopped")
