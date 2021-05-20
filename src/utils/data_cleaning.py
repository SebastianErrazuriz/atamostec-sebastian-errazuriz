from pandas.core.frame import DataFrame
from scipy import signal
from datetime import time


def sum_by_hour(df: DataFrame, time_col='TimeStamp'):
    '''
    Sum the values grouping by hour

    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.
    time_col : TYPE, optional
        DESCRIPTION. The default is 'TimeStamp'.

    Returns
    -------
    df_hr : DataFrame
        Same dataframe with a new column with the hours and the other
        values are sumed dor each hour.

    '''
    # df with hours
    df_hr = df.copy(deep=True)
    df_hr.reset_index(inplace=True, drop=False)
    df_hr['hour'] = df_hr[time_col].dt.hour
    df_hr = df_hr.groupby(['hour']).sum()

    return df_hr


def mean_by_hour(df: DataFrame, time_col='TimeStamp'):
    '''
    Mean the values grouping by hour

    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.
    time_col : TYPE, optional
        DESCRIPTION. The default is 'TimeStamp'.

    Returns
    -------
    df_hr : DataFrame
        Same dataframe with a new column with the hours and the other
        values are sumed dor each hour.

    '''
    # df with hours
    df_hr = df.copy(deep=True)
    df_hr.reset_index(inplace=True, drop=False)
    df_hr['hour'] = df_hr[time_col].dt.hour
    df_hr = df_hr.groupby(['hour']).mean()

    return df_hr


def low_watt(watt, umbral=40.0):
    '''
    Returns cero for watts under the umbral

    Parameters
    ----------
    watt : TYPE
        DESCRIPTION.
    umbral : TYPE, optional
        DESCRIPTION. The default is 40.0.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''

    if watt <= umbral:
        return 0
    else:
        return watt


def filter_pass_hour(watt, time, hour_umbral=time(21, 56, 55, 0)):
    '''
    Returns cero for values pass the hour

    Parameters
    ----------
    watt : TYPE
        DESCRIPTION.
    umbral : TYPE, optional
        DESCRIPTION. The default is 40.0.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    print(time.dt.time)
    if time.dt.time >= hour_umbral:
        return 0
    else:
        return watt


def filter_filtfilt(data, pole_lowpass=5.0, nyq_freq=0.1):
    '''
    Applys a digital filter foward and backward to a signal. Butter is a
    Butterworth digital and analog filter design

    Parameters
    ----------
    data : DataFrame column
        df column that we want to filter.
    pole_lowpass : float, optional
        Lowpass Butterwoth. The default is 3.0.
    nyq_freq : float, optional
        Cutoff of x times the Nyquist frequency. The default is 0.1.

    Returns
    -------
    filtered : TYPE
        DESCRIPTION.

    '''
    # apply a 3-pole lowpass filter at 0.1x Nyquist frequency
    a, b = signal.butter(pole_lowpass, nyq_freq)
    filtered = signal.filtfilt(a, b, data)

    return filtered
