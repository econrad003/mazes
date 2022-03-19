"""__init.py__ - initialization of mazelib package
Copyright 2022 by Eric Conrad

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

FIX_PATH = True
DEBUG = False

if DEBUG:
    print(f'INFO: Debugging set in file {__file__}.')

    # Append the package directory to the module search path...
    # This will allow the maze modules to import any needed modules.

import sys, os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

if FIX_PATH and not dir_path in sys.path:
    if DEBUG:
        print(f'INFO: Adding {dir_path} to module search path.')
    sys.path.append(dir_path)   # add the directory to the search path

    # import the basic building blocks


# End of __init__.py
