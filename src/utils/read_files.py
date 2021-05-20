from datetime import datetime
import pandas as pd
from pandas.core.frame import DataFrame


def read_txt_file(path: str) -> DataFrame:
    '''
    Read txt file and return a dataframe object

    Parameters
    ----------
    path : str
        location of the file.

    Returns
    -------
    DataFrame
        Resulting dataframe.
    '''
    custom_date_parser = lambda x: datetime.strptime(x, "%Y_%m_%d %H:%M:%S")

    # Read the file
    df = pd.read_csv(path, sep=';', parse_dates=['TimeStamp'],
                     date_parser=custom_date_parser, decimal=',',
                     index_col='TimeStamp')

    return df
