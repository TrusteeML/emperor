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
    runCompare(CAR_PATH, CAR_HAS_HEADER, CAR_DATA_TYPES, CAR_IS_CLASSIFY, CAR_N_DATA_MATRIX_COLS, CAR_OUTPUT)
