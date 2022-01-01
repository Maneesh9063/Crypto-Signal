""" Custom Indicator Increase In  Volume
"""

import numpy as np
from scipy import stats
import requests as rq

from analyzers.utils import IndicatorUtils
from analyzers.informants import *



class IIV(IndicatorUtils):
    def analyze(self, historical_data, signal=['iiv'], hot_thresh=10, cold_thresh=0):
        """Performs an analysis about the increase in volumen on the historical data

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to iiv. The indicator line to check hot against.
            hot_thresh (float, optional): Defaults to 10. 
            cold_thresh: Unused


        Returns:
            pandas.DataFrame: A dataframe containing the indicator and hot/cold values.
        """

        dataframe = self.convert_to_dataframe(historical_data)

        # z = np.abs(stats.zscore(dataframe['volume']))
        # filtered = dataframe.volume[(z < 3)]

        # previous_mean = filtered.mean()

        dataframe[signal[0]] = dataframe['volume'].pct_change()*100
        # dataframe[signal[0]] = dataframe['volume']/ previous_mean

        dataframe["SMA"] =  dataframe['close'].rolling(9).mean()
        dataframe['is_hot'] = dataframe[signal[0]] >= hot_thresh 
        dataframe ["sma_crossed"] = dataframe["close"] > dataframe["SMA"] 
        dataframe["liquidity"] = dataframe["close"]*dataframe["volume"]
        dataframe["liq_bool"] = dataframe["liquidity"] > 3500
        x = dataframe["liq_bool"].tail(12).all()
        dataframe['is_cold'] = False
        # dataframe['is_hot'] = True

        dataframe['is_hot'] = dataframe['is_hot'] & dataframe['sma_crossed'] 
        dataframe['is_hot'] = dataframe['is_hot'] & x

        # print(dataframe)
        # print(x)
        return dataframe
