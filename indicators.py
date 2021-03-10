import logging
from typing import Tuple
import talib
import numpy as np
import math

from ticker import Ticker


class Indicators:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.averages_low = []
        self.averages_high = []
        self.average_period_low = 0
        self.average_period_high = 0

    def add_value_to_move_average_data(self, last: float, period: list):
        self.average_period_low = min(period)
        self.average_period_high = max(period)
        
        self.averages_low.append(last)
        self.averages_high.append(last)
        

    def calculate_simple_move_average(self, kind: str = 'low') -> Tuple:

        if kind == 'low':
            period = self.average_period_low
            averages = self.averages_low
        else:
            period = self.average_period_high
            averages = self.averages_high
            
        
        np_averages = np.array(averages)
        
        sma = talib.SMA(np_averages, period)    

        sma_previous = sma[-2] if len(sma) >= period else 0
        sma_current = sma[-1] if len(sma) >= period else 0

        # print('Previous: {0}'.format(sma_previous))
        # print('Current: {0}'.format(sma_current))


        return sma_previous, sma_current


    