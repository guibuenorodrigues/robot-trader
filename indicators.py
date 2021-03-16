import logging
from typing import Tuple
from numpy.lib.function_base import average
import pandas as pd
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
            
        
        numbers_series = pd.Series(averages)
        windows = numbers_series.rolling(period)
        moving_averages = windows.mean()

        moving_averages_list = moving_averages.tolist()

        sma_previous = moving_averages_list[-2] if len(moving_averages_list) >= period else 0
        sma_current = moving_averages_list[-1] if len(moving_averages_list) >= period else 0

        return sma_previous, sma_current


    def __index_in_list(self, a_list: list, index: int) -> bool:
    
        print((index < len(a_list)))

        return (index < len(a_list))

    