# Copyright 2013, 2014, 2015, 2016, 2017 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

from . import minivenv, projectinfo
import os, subprocess, sys, tests

def main_tests():
    runtests(projectinfo.ProjectInfo(os.getcwd()), sys.argv[1:])

def runtests(info, args):
    testspath = tests.__file__
    if testspath.endswith('.pyc'):
        testspath = testspath[:-1]
    for pyversion in info['pyversions']:
        # Equivalent to running tests.py directly but with one fewer process launch:
        subprocess.check_call([minivenv.executable(info, pyversion), testspath] + args)
