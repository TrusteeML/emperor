from FeatureExtractor import *
from KitNET.KitNET import KitNET

# MIT License
#
# Copyright (c) 2018 Yisroel mirsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Kitsune:
    def __init__(
        self,
        file_path,
        limit,
        max_autoencoder_size=10,
        FM_grace_period=None,
        AD_grace_period=10000,
        learning_rate=0.1,
        hidden_ratio=0.75,
    ):
        # init packet feature extractor (AfterImage)
        self.FE = FE(file_path, limit)

        # init Kitnet
        self.AnomDetector = KitNET(
            self.FE.get_num_features(),
            max_autoencoder_size,
            FM_grace_period,
            AD_grace_period,
            learning_rate,
            hidden_ratio,
        )

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_path(self, file_path, limit):
        # set packet feature extractor (AfterImage)
        self.FE = FE(file_path, limit)

    def proc_next_packet(self):
        # create feature vector
        x = self.FE.get_next_vector()
        if len(x) == 0:
            return -1  # Error or no packets left

        # process KitNET
        # will train during the grace periods, then execute on all the rest.
        return self.AnomDetector.process(x)

    def get_next_vector(self):
        return self.FE.get_next_vector()

    def predict(self, x):
        # process KitNET
        if np.array(x).ndim == 1:
            # will train during the grace periods, then execute on all the rest.
            return self.AnomDetector.process(x)

        y = []
        for x_it in np.array(x):
            y.append(self.AnomDetector.process(x_it))

        return np.array(y)
