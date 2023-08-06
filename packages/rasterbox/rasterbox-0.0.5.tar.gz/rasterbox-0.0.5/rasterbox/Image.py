import numpy as np
import  matplotlib.pyplot as plt
from rasterbox.utilities import Misc
from rasterbox.utilities import DataManip


class Image(object):
    def __init__(self, bin=None, nparray=None):
        if nparray is None:
            samples, lines, bands, data = Misc.read_binary(bin)
            self.samples, self.lines, self.bands = \
                int(samples), int(lines), int(bands)
            self._Data = data.reshape(self.lines * self.samples, self.bands)
            self.__build_rgb()
        else:
            self._Data = nparray


    def __build_rgb(self):
        arr = np.zeros((self.lines, self.samples, 3))

        # data has to switch around for matplotlib
        tmp = self._Data.reshape(self.bands, self.lines * self.samples)
        for i in range(0, 3):
            arr[:, :, i] = tmp[3 - i, :].reshape((self.lines, self.samples))

        for i in range(0, 3):
            arr[:, :, i] = DataManip.rescale(arr[:, :, i])

        del tmp
        self.rgb = arr

    def spatial(self):
        return self._Data.reshape((self.samples,self.lines,self.bands))


    def Data(self):
        return self._Data


    def showplot(self):
        plt.imshow(self.rgb)
        plt.tight_layout()
        plt.show()