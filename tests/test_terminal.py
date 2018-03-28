#!/usr/bin/python3
# Validate Terminal handling
#
# Copyright (C) 2018 Canonical, Ltd.
# Author: Mathieu Trudel-Lapierre <mathieu.trudel-lapierre@canonical.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import fcntl
import sys
import os
import termios
import unittest

import netplan.terminal


class TestTerminal(unittest.TestCase):

    def setUp(self):
        self.terminal = netplan.terminal.Terminal(sys.stdin.fileno())

    def test_echo(self):
        orig_attrs = termios.tcgetattr(self.terminal.fd)
        self.terminal.disable_echo()
        attrs = termios.tcgetattr(self.terminal.fd)
        self.assertFalse(attrs[3] & termios.ECHO)
        self.terminal.enable_echo()
        attrs = termios.tcgetattr(self.terminal.fd)
        self.assertTrue(attrs[3] & termios.ECHO)
        self.assertEquals(orig_attrs, attrs)

    def test_nonblocking_io(self):
        orig_flags = flags = fcntl.fcntl(self.terminal.fd, fcntl.F_GETFL)
        self.assertFalse(flags & os.O_NONBLOCK)
        self.terminal.enable_nonblocking_io()
        flags = fcntl.fcntl(self.terminal.fd, fcntl.F_GETFL)
        self.assertTrue(flags & os.O_NONBLOCK)
        self.assertNotEquals(flags, orig_flags)
        self.terminal.disable_nonblocking_io()
        flags = fcntl.fcntl(self.terminal.fd, fcntl.F_GETFL)
        self.assertFalse(flags & os.O_NONBLOCK)
        self.assertEquals(flags, orig_flags)

    def test_reset(self):
        self.terminal.enable_nonblocking_io()
        flags = fcntl.fcntl(self.terminal.fd, fcntl.F_GETFL)
        self.assertTrue(flags & os.O_NONBLOCK)
        self.terminal.reset()
        flags = fcntl.fcntl(self.terminal.fd, fcntl.F_GETFL)
        self.assertFalse(flags & os.O_NONBLOCK)