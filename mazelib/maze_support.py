"""maze_support.py - implementation of support classes
Copyright 2022 by Eric Conrad

DESCRIPTION

    Implemented here are a number of support classes:

                queuing classes
        Unqueue - a general queuing class
            Queue - a FIFO (first in, first out) queuing class
            Stack - a LIFO (last in, first out) queuing class
            Heap - a BIFO (best in, first out) priority queue

REFERENCES

    [1] Jamis Buck.  Mazes for programmers.  2015, the Pragmatic
        Bookshelf.  ISBN-13: 978-1-68050-055-4.

LICENSE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see
        <https://www.gnu.org/licenses/>.
"""

from random import random, randrange
import heapq

class Unqueue(object):
    """a generalized queuing class - random in, first out"""

    def __init__(self, *args, **kwargs):
        """constructor"""
        self._queue = []
        self._args = args
        self._kwargs = kwargs

        self.initialize()

    def initialize(self):
        """additional initialization"""
        pass          # stub

    def enter(self, *args, **kwargs):
        """package the arguments and put them in into the queue

        OPTIONAL ARGUMENTS

            *args - these are packaged as a tuple and placed into the
                end of the queue

        KEYWORD ARGUMENTS

            These are ignored by the Unqueue class, but may be processed
            by derived classes.
        """
        package = args
        self._queue.append(package)

    def serve(self):
        """remove a random package from the queue"""
        i = randrange(len(self._queue))
        package = self._queue[i]
        self._queue = self._queue[:i] + self._queue[i+1:]
        return package

    def __len__(self):
        """return the number of entries"""
        return len(self._queue)

    @property
    def isEmpty(self):
        """determine whether the queue is empty"""
        return not self._queue

class Queue(Unqueue):
    """a standard FIFO queue"""

    def serve(self):
        """remove the first package from the queue"""
        return self._queue.pop(0)

class Stack(Unqueue):
    """a standard LIFO stack"""

    def serve(self):
        """remove the last package from the queue"""
        return self._queue.pop()

class Heap(Unqueue):
    """a min-priority queue implemented as a heap"""

    def initialize(self):
        """additional initialization

        KEYWORD ARGUMENTS (passed from __init__)

            interval - an interval to be used for generating random
                priorities (default: [1,2])

        To insure that the priorities are unique, order of entry is
        used to settle any conflicts with equal priorities.
        """
        interval = self._kwargs.get('interval', [1,2])
        self._a = interval[0]
        self._b = interval[1]
        self._index = 0         # order of entry

    def enter(self, *args, **kwargs):
        """package the arguments and put them in into the queue

        OPTIONAL ARGUMENTS

            *args - these are packaged as a tuple and placed into the
                end of the queue

        KEYWORD ARGUMENTS

            priority - if present, it will be used; if absent, the
                priority is a random value in the interval provided to
                the constructor
        """
        a, b = self._a, self._b
        priority = kwargs.get('priority', (b-a)*random() + a)
        package = (priority, self._index, args)
        self._index += 1        # order of entry
        heapq.heappush(self._queue, package)

    def serve(self):
        """remove the highest priority package from the queue

        The highest priority has the smallest value.
        """
        package = heapq.heappop(self._queue)
        return package[2]

# end of maze_support.py
