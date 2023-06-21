import numpy as np
import pandas as pd

import statsmodels.api as sm
from statsmodels.formula.api import ols
import pandas_datareader as dr

import warnings
warnings.filterwarnings("ignore")

class CAPM(object):

    def __init__(self, ticker, index, start, end, api='yahoo'):
        self.ticker = ticker
        self.index = index
        self.start = start
        self.end = end
        self.api = api

        self.extrair_dados()
        self.processar_dados()
        self.treinar_regressao_linear()
    
    def extrair_dados(self):
        tickers = [self.index, self.ticker]
        ativos = []
        for ticker in tickers:
            try:
                cotacoes = dr.DataReader(ticker, self.api, self.start, self.end)["Adj Close"]
                cotacoes = pd.DataFrame(cotacoes)
                cotacoes.columns = [ticker]
                ativos.append(cotacoes)
            except:
                pass
            self.base_ativos = pd.concat(ativos, axis = 1)
        self.base_ativos.sort_index(inplace = True)
    
    def processar_dados(self):
        # Ficamos apenas com os retornos
        self.base_ativos = pd.DataFrame(self.base_ativos.pct_change())
        self.base_ativos.dropna(inplace = True)

        # Calcule o retorno esperado do mercado usando os dados históricos
        self.market_mean_return = np.mean(self.base_ativos.iloc[:,0])

        # Calcule a matriz de covariância para o mercado e o ativo
        self.cov_matrix = np.cov(self.base_ativos.iloc[:,0], self.base_ativos.iloc[:,1])

        # Extraia a covariância entre o mercado e o ativo
        self.market_asset_cov = self.cov_matrix[0,1]

        # Calcule o beta do ativo (ou seja, a sensibilidade dos retornos do ativo aos retornos do mercado)
        self.beta = self.market_asset_cov / np.var(self.base_ativos.iloc[:,0])
    
    def treinar_regressao_linear(self):
        x_train = sm.add_constant(self.base_ativos.iloc[:,0])
        y_train = self.base_ativos.iloc[:,1]

        self.lr_sm = sm.OLS(y_train, x_train).fit()

    def calcular_retorno_esperado(self, selic):
        return selic + self.beta * (self.market_mean_return - selic)
    
    def obter_sumario(self):
        return self.lr_sm.summary()


