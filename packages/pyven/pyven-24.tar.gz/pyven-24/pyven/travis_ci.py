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

from . import projectinfo, checks
import os, subprocess

class Workspace:

    def __init__(self, workspace):
        self.workspace = workspace

    def checkoutifnecessary(self, project):
        path = os.path.join(self.workspace, project)
        if not os.path.exists(path): # Allow for diamond dependencies.
            subprocess.check_call(['git', 'clone', '-b', 'master', "https://github.com/combatopera/%s.git" % project], cwd = self.workspace)
        for project2 in projectinfo.ProjectInfo(path)['projects']:
            self.checkoutifnecessary(project2)

def main_travis_ci():
    workspace = Workspace(os.path.dirname(os.getcwd()))
    info = projectinfo.ProjectInfo(os.getcwd())
    for project in info['projects']:
        workspace.checkoutifnecessary(project)
    with open('.gitignore', 'a') as f:
        f.write('/.pyven/\n')
    checks.everyversion(info, [])
