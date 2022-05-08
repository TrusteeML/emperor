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

# Main code

from .runCompare import *
from ..data.consts import *

if __name__ == "__main__":
    runCompare(POST_OPERATIVE_PATH, POST_OPERATIVE_HAS_HEADER, POST_OPERATIVE_DATA_TYPES, POST_OPERATIVE_IS_CLASSIFY, POST_OPERATIVE_N_DATA_MATRIX_COLS, POST_OPERATIVE_OUTPUT)
