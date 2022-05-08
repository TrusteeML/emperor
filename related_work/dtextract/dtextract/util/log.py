# Copyright 2015-2016 Stanford University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Logging with optional verbosity levels

# Verbosity global constants
SILENT = 0
ERROR = 1
WARN = 2
INFO = 3
DEBUG = 4

# Current verbosity
_curVerbosity = INFO

# Output file
_output = None

# Sets the current output file.
#
# parameters/returns:
#  output : str | None (output filename)


def setCurOutput(output):
    global _output
    _output = output
    f = open(_output, 'w')
    f.close()

# Sets the current verbosity (defaults to standard).
#
# parameters/returns:
#  verbosity : int


def setCurVerbosity(verbosity):
    global _curVerbosity
    _curVerbosity = verbosity

# Prints the given message if its verbosity is
# at most the current setting.
#
# parameters/returns:
#  msg : str
#  verbosity : int


def log(msg, verbosity):
    if verbosity <= _curVerbosity:
        print(msg)
        if not _output is None:
            f = open(_output, 'a')
            f.write("{}\n".format(msg))
            f.close()
