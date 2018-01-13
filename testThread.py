# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 11:43:59 2018

@author: Administrator
"""

import time
from threading import Thread, Event
import random

items = []
event = Event()


class Consumer(Thread):
    def __init__(self, items, event):
        Thread.__init__(self)
        self.items = items
        self.event = event

    def run(self):
        while True:
            time.sleep(2)
            self.event.wait()
            item = self.items.pop()
            print("Consumer notify: %d poped from list by %s"
                  %(item, self.name))

class Producer(Thread):
    def __init__(self, items, event):
        Thread.__init__(self)
        self.items = items
        self.event = event

    def run(self):
        global item
        for i in range(10):
            time.sleep(2)
            item = random.randint(0, 256)
            self.items.append(item)
            print ("Producer nofity: item N %d appended to list by %s"
                   % (item, self.name))
            print ("Producer notify: event set by %s "
                   % self.name)
            self.event.set()
            print("Produce notify: event clear by %s\n"
                  % self.name)
            self.event.clear()


if __name__ == "__main__":
    producer = Producer(items, event)
    consumer = Consumer(items, event)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()