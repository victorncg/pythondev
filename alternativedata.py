# MODULE FOR OBTAINING ALTERNATIVE DATA

# SOME OF THE ALTERNATIVE DATA WE CAN OBTAIN FROM THIS MODULE
# IBOV Composition
# Google Trends
# CVM
# B3
# S&P 500

import pandas as pd

import functools
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def _logging_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper


# Função para extrair os dados do IBOV
@_logging_error
def _parse_ibov():
    
    try:
        
        url = 'https://raw.githubusercontent.com/victorncg/financas_quantitativas/main/IBOV.csv'
        df = pd.read_csv(url, encoding='latin-1', sep='delimiter', header=None, engine='python')
        df = pd.DataFrame(df[0].str.split(';').tolist())
        
        return df
        
    except:
        
        print("An error occurred while parsing data from IBOV.")



@_logging_error
def _standardize_ibov():
    
    try:
        
        df = _parse_ibov()
        df.columns = list(df.iloc[1])
        df = df[2:][['Código','Ação', 'Tipo', 'Qtde. Teórica','Part. (%)']]
        df.reset_index(drop=True, inplace=True)
        
        return df
        
    except:
        
        print("An error occurred while manipulating data from IBOV.")


def _standardize_sp500():
    
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    
    df = table[0]

    return df


def _adapt_index(index:object, assets:object = 'all', mode:object = 'df', reduction:bool = True):
    '''
    This function processes the data from the latest composition of either IBOV or S&P 500. It is updated every 4 months.
    
    Parameters
    ----------
    index : choose the index to be returned, if IBOV or S&P 500
    ativos : you can pass a list with the desired tickets. Default = 'all'.
    mode: you can return either the whole dataframe from B3, or just the list containing the tickers which compose IBOV. Default = 'df'.
    reduction: you can choose whether the result should come with the reduction and theorical quantitiy provided by B3. Default = True.
    
    '''

    
    if index == 'ibov':
        
        df = _standardize_ibov()
        
        if reduction == False:
            df = df[:-2]
    
        if assets != 'all':
            df = df[df['Código'].isin(assets)]    
        
        if mode == 'list':
            df = list(df.Código)
    
    if index == 'sp500':
        
        df = _standardize_sp500()

        if assets != 'all':
            df = df[df['Symbol'].isin(assets)]

        if mode == 'list':
            df = list(df.Symbol)

    return df


@_logging_error
def index_composition(index:object, assets:object = 'all', mode:object = 'df', reduction:bool = True):
    '''
    This function captures the latest composition of either IBOV or S&P 500. It is updated every 4 months.
    
    Parameters
    ----------
    index : choose the index to be returned, if IBOV or S&P 500
    ativos : you can pass a list with the desired tickets. Default = 'all'.
    mode: you can return either the whole dataframe from B3, or just the list containing the tickers which compose IBOV. Default = 'df'.
    reduction: you can choose whether the result should come with the reduction and theorical quantitiy provided by B3. Default = True.
    
    '''
    
    df = _adapt_index(index, assets, mode, reduction)

    return df



