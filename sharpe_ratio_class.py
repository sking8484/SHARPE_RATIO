
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web



class SharpeArray:
    def __init__(self, num_ports, portfolio_list):
        self.num_ports = num_ports
        self.portfolio_list = portfolio_list
        print('>>> YOU HAVE INSTANTIATED A SHARPE ARRAY CALCULATION.... \n PLEASE CALL THE GET DATA FUNCTION')
        self.stock_data = pd.DataFrame()

        self.all_weights = np.zeros((self.num_ports, len(self.portfolio_list)))
        self.return_array = np.zeros(self.num_ports)
        self.vol_array = np.zeros(self.num_ports)
        self.sharpe_array = np.zeros(self.num_ports)




    def get_data(self):
        print('>>> GETTING DATA FOR ' + str(self.portfolio_list))
        for x in self.portfolio_list:
            intermit_df = web.DataReader(x.upper(), 'iex', start = '2014-01-01')
            intermit_df = intermit_df[['close']]
            intermit_df.columns = [x]
            self.stock_data = pd.concat([self.stock_data, intermit_df], axis = 1)
        log_returns = np.log(self.stock_data/self.stock_data.shift(1))
        self.calculate_sharpe(log_returns)
    def calculate_sharpe(self, log_returns):

        for portfolio in range(self.num_ports):
            weights = np.array(np.random.random(len(self.portfolio_list)))
            weights = weights/np.sum(weights)


            self.all_weights[portfolio,:] = weights

            self.return_array[portfolio] = np.sum((log_returns.mean( ) *weights) * 252)
            self.vol_array[portfolio] = np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 252, weights)))
            self.sharpe_array[portfolio] = self.return_array[portfolio] /self.vol_array[portfolio]
            if portfolio %100 ==0:
                print('>>> CALCULATING THE SHARPE RATIO FOR PORTFOLIO NUMBER: ' + str(portfolio))

        max_sharpe = self.sharpe_array.argmax()
        optimized_weights = self.all_weights[max_sharpe ,:]
        max_rets = self.return_array[max_sharpe]
        max_vol = self.vol_array[max_sharpe]

        self.plot(optimized_weights, max_rets, max_vol)
    def plot(self, optimized_weights, max_rets, max_vol):
        print('>>> PLOTTING')
        plt.figure(figsize = (20 ,10))
        plt.scatter(self.vol_array, self.return_array, c = self.sharpe_array)
        plt.colorbar()
        plt.scatter(max_vol, max_rets, c = 'r')
        plt.xlabel('VOLATILITY')
        plt.ylabel('RETURNS')
        plt.title('SHARPE MARKOWITZ BULLET')
        plt.show()
