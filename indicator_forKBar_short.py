import numpy as np
import datetime

class KBar():
    def __init__(self, date, cycle=1):
        self.TAKBar = {}
        self.TAKBar['time'] = np.array([])
        self.TAKBar['open'] = np.array([])
        self.TAKBar['high'] = np.array([])
        self.TAKBar['low'] = np.array([])
        self.TAKBar['close'] = np.array([])
        self.TAKBar['volume'] = np.array([])
        self.current = datetime.datetime.strptime(date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.cycle = datetime.timedelta(minutes=cycle)

    def AddPrice(self, time, open_price, close_price, low_price, high_price, volume):
        if len(self.TAKBar['time']) == 0:
            self.TAKBar['time'] = np.array([time])
            self.TAKBar['open'] = np.array([open_price])
            self.TAKBar['high'] = np.array([high_price])
            self.TAKBar['low'] = np.array([low_price])
            self.TAKBar['close'] = np.array([close_price])
            self.TAKBar['volume'] = np.array([volume])
            return 1
        
        if time <= self.current:
            if len(self.TAKBar['close']) == 0:
                self.TAKBar['time'] = np.append(self.TAKBar['time'], time)
                self.TAKBar['open'] = np.append(self.TAKBar['open'], open_price)
                self.TAKBar['high'] = np.append(self.TAKBar['high'], high_price)
                self.TAKBar['low'] = np.append(self.TAKBar['low'], low_price)
                self.TAKBar['close'] = np.append(self.TAKBar['close'], close_price)
                self.TAKBar['volume'] = np.append(self.TAKBar['volume'], volume)
            else:
                self.TAKBar['close'][-1] = close_price
                self.TAKBar['volume'][-1] += volume
                self.TAKBar['high'][-1] = max(self.TAKBar['high'][-1], high_price)
                self.TAKBar['low'][-1] = min(self.TAKBar['low'][-1], low_price)
            return 0
        
        else:
            while time > self.current:
                self.current += self.cycle
            self.TAKBar['time'] = np.append(self.TAKBar['time'], self.current)
            self.TAKBar['open'] = np.append(self.TAKBar['open'], open_price)
            self.TAKBar['high'] = np.append(self.TAKBar['high'], high_price)
            self.TAKBar['low'] = np.append(self.TAKBar['low'], low_price)
            self.TAKBar['close'] = np.append(self.TAKBar['close'], close_price)
            self.TAKBar['volume'] = np.append(self.TAKBar['volume'], volume)
            return 1

    def GetTime(self):
        return self.TAKBar['time']

    def GetOpen(self):
        return self.TAKBar['open']

    def GetHigh(self):
        return self.TAKBar['high']

    def GetLow(self):
        return self.TAKBar['low']

    def GetClose(self):
        return self.TAKBar['close']

    def GetVolume(self):
        return self.TAKBar['volume']

# 如果需要使用 talib 的技術指標函數，請根據需求解除以下函數的註解
# 並確保已從 talib.abstract 中載入相應的函數

# def GetMA(self, n, matype):
#     return MA(self.TAKBar, n, matype)

# def GetSMA(self, n):
#     return SMA(self.TAKBar, n)

# def GetWMA(self, n):
#     return WMA(self.TAKBar, n)

# def GetEMA(self, n):
#     return EMA(self.TAKBar, n)

# def GetBBands(self, n):
#     return BBANDS(self.TAKBar, n)

# def GetRSI(self, n):
#     return RSI(self.TAKBar, n)

# def GetKD(self, rsv, k, d):
#     return STOCH(self.TAKBar, fastk_period=rsv, slowk_period=k, slowd_period=d)

# def GetWILLR(self, tp=14):
#     return WILLR(self.TAKBar, timeperiod=tp)

# def GetBIAS(self, tn=10):
#     mavalue = MA(self.TAKBar, timeperiod=tn, matype=0)
#     return (self.TAKBar['close'] - mavalue) / mavalue
