#!/usr/bin/env python3
# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************
from time import sleep
import time
from brain_pycore.zmq import (
    ZmqPublisherThread, ZmqSubscriberThread, ZmqServerThread, ZmqClientThread)
import unittest


class TestZmq(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.PORT = 55580
        cls.TOPIC = "Hot Topic"

    def test_pub_sub(self):

        def publisher_callback():
            return f"Hello {time.time()}"

        def subscriber_callback(msg: str):
            print(msg)

        pub = ZmqPublisherThread(self.PORT, self.TOPIC, publisher_callback)
        pub.start()
        sub = ZmqSubscriberThread(self.PORT, self.TOPIC,
                                  callback=subscriber_callback)
        sub.start()

        sleep(5)

        pub.stop()
        sub.stop()

    def test_server_client(self):

        def server_cb(req):
            return "Hello!"

        ser = ZmqServerThread(self.PORT, server_cb)
        ser.start()

        cli = ZmqClientThread(self.PORT)
        cli.start()

        for i in range(5):
            r = cli.send("World?")
            assert r == "Hello!"
            sleep(1)

        cli.stop()
        ser.stop()


if __name__ == '__main__':
    unittest.main()
