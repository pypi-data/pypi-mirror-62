'''
Experimental..

#TODO:
 - format plot
 - ensure it's working correctly
 - error message is not raised when datapoints are less than fit order
'''

import os

import numpy as np
import matplotlib.pyplot as plt

from pysprint.api.dataset import Dataset
from pysprint.core.evaluate import spp_method
from pysprint.utils import print_disp
from pysprint.api.exceptions import DatasetError


__all__ = ['SPPMethod']

class SPPMethod:
    def __init__(self, ifg_names, sam_names=None, ref_names=None, **kwargs):
        self.ifg_names = ifg_names
        if sam_names:
            self.sam_names = sam_names
        else:
            self.sam_names = None
        if ref_names:
            self.ref_names = ref_names
        else:
            self.ref_names = None
        self._validate()
        if self.sam_names:
            if not len(self.ifg_names) == len(self.sam_names):
                raise DatasetError('Missmatching length of files.')
        if self.ref_names:
            if not len(self.ifg_names) == len(self.ref_names):
                raise DatasetError('Missmatching length of files.')
        self.idx = 0
        self.skiprows = kwargs.get('skiprows', 8)
        self.decimal = kwargs.get('decimal', ',')
        self.sep = kwargs.get('sep', ';')
        self.meta_len = kwargs.get('meta_len', 4)

        self._delay = {}
        self._positions = {}


    def __len__(self):
        return len(self.ifg_names)

    def __iter__(self):
        return self

    def __str__(self):
        return f'{type(self).__name__} object\nInterferogram count : {len(self)}'

    def __next__(self):
        if self.idx < len(self):
            try:
                d = Dataset.parse_raw(
                    self.ifg_names[self.idx], self.sam_names[self.idx], self.ref_names[self.idx],
                    skiprows=self.skiprows, decimal=self.decimal, sep=self.sep, meta_len=self.meta_len
                    )
            except TypeError:
                d = Dataset.parse_raw(
                    self.ifg_names[self.idx], skiprows=self.skiprows, decimal=self.decimal, 
                    sep=self.sep, meta_len=self.meta_len
                    )
            self.idx += 1
            return d
        raise StopIteration


    def __getitem__(self, key):
        try:
            dataframe = Dataset.parse_raw(
                self.ifg_names[key], self.sam_names[key], self.ref_names[key],
                skiprows=self.skiprows, decimal=self.decimal, sep=self.sep, meta_len=self.meta_len
                )
        except (TypeError, ValueError):
            dataframe = Dataset.parse_raw(
                self.ifg_names[key], skiprows=self.skiprows, decimal=self.decimal, sep=self.sep,
                 meta_len=self.meta_len
                 )
        return dataframe

    def _validate(self):
        for filename in self.ifg_names:
            if os.path.exists(filename):
                pass
            else:
                raise FileNotFoundError(f'''File named '{filename}' is not found.''')
        if self.sam_names:
            for sam in self.sam_names:
                if os.path.exists(sam):
                    pass
                else:
                    raise FileNotFoundError(f'''File named '{sam}' is not found.''')
        if self.ref_names:
            for ref in self.ref_names:
                if os.path.exists(ref):
                    pass
                else:
                    raise FileNotFoundError(f'''File named '{ref}' is not found.''')


    def set_data(self, delay, position):
        self._delay[self.idx] = delay
        self._positions[self.idx] = position

    @print_disp
    def calculate(self, reference_point, order=2, show_graph=False):
        delays = np.concatenate([_ for _ in self._delay.values()]).ravel()
        positions = np.concatenate([_ for _ in self._positions.values()]).ravel()
        x, y, dispersion, dispersion_std, bf = spp_method(
            delays, positions, reference_point=reference_point, fitOrder=order, from_raw=True)
        if show_graph:
            plt.plot(x, y, 'o')
            try:
                plt.plot(x, bf, 'r--', zorder=1)
            except Exception as e:
                print(e)
            plt.grid()
            plt.show()
        return dispersion, dispersion_std, bf

    @property
    def info(self):
        self._info = f'Data is recorded from {len(self._delay)} interferograms ({len(self)} availabe in total)'
        return self._info
    
    
# # EXAMPLE USAGE
# if __name__ == '__main__':

#     i = [f"D:/Python/mrs/URES0{i:03d}.trt" for i in range(56, 81, 3)]
#     s = [f"D:/Python/mrs/URES0{i:03d}.trt" for i in range(57, 82, 3)]
#     r = [f"D:/Python/mrs/URES0{i:03d}.trt" for i in range(58, 83, 3)]

#     ifgs = SPPMethod(i, s, r)

#     for ifg in ifgs:
#         ifg.chdomain()
#         ifg.slice(start=1.95, stop=4.4)
#         ifg.open_SPP_panel()
#         ifgs.set_data(*ifg.emit())

#     ifgs.calculate(2.355, order=2, show_graph=True)






    










