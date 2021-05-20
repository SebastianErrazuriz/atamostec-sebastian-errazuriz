import matplotlib.pyplot as plt
import mplcursors
from pandas.core.frame import DataFrame
import numpy as np


def plot_irradiance(df: DataFrame, title=None):
    '''
    Plot irradiance for all sensors for a panel

    Parameters
    ----------
    df : DataFrame
        Sensor cell dataframe.
    title : str
        title. The default is None.

    '''

    fig, ax = plt.subplots()
    for column in df:
        if '(w.m-2)' in column:
            ax.plot(df[column], label=column)
            if title:
                ax.set_title(title, fontsize=24)
    # Add legend to  click
    mplcursors.cursor(highlight=True).\
        connect("add", lambda sel:
                sel.annotation.set_text(sel.artist.get_label()))
    plt.tight_layout()
    plt.show()


def plot_temp(df: DataFrame, title=None):
    '''
    Plot temperature for all sensors for a panel

    Parameters
    ----------
    df : DataFrame
        Sensor cell dataframe.
    title : str
        title. The default is None.

    '''

    fig, ax = plt.subplots()
    for column in df:
        if '(C)' in column:
            ax.plot(df[column], label=column)
            if title:
                ax.set_title(title, fontsize=24)
    # Add legend to  click
    mplcursors.cursor(highlight=True).\
        connect("add", lambda sel:
                sel.annotation.set_text(sel.artist.get_label()))
    plt.tight_layout()
    plt.show()


def plot_watt(df: DataFrame, title=None):
    '''
    Plot watt for all sensors for a panel

    Parameters
    ----------
    df : DataFrame
        Sensor cell dataframe.
    title : str
        title. The default is None.

    '''

    fig, ax = plt.subplots()
    for column in df:
        if '(W)' in column:
            ax.plot(df[column], label=column)
            if title:
                ax.set_title(title, fontsize=24)
    # Add legend to  click
    mplcursors.cursor(highlight=True).\
        connect("add", lambda sel:
                sel.annotation.set_text(sel.artist.get_label()))
    plt.tight_layout()
    plt.show()


def plot_sensor(df: DataFrame, sensor_name: str, title=None):
    '''
    Plot irradiance and temperature for a specific sensor in cell panel

    Parameters
    ----------
    df : DataFrame
        Sensor cell dataframe.
    sensor_name : str
        sensors name.

    '''

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    for column in df:
        if '(C)' in column and sensor_name in column:
            ax.plot(df[column], label=column, color='blue')
        if '(w.m-2)' in column and sensor_name in column:
            ax2.plot(df[column], label=column, color='red')
    # Add legend to  click
    mplcursors.cursor(highlight=True).\
        connect("add", lambda sel:
                sel.annotation.set_text(sel.artist.get_label()))
    plt.tight_layout()
    plt.show()


def plot_clusters(df: DataFrame, title=None):
    '''
    Plot irradiance for all clusters in a panel

    Parameters
    ----------
    df : DataFrame
        Sensor cell dataframe.
    title : str
        title. The default is None.

    '''

    fig, ax = plt.subplots()
    for column in df:
        if 'c' in column:
            ax.plot(df[column], label=column)
            if title:
                ax.set_title(title, fontsize=24)
    # Add legend to  click
    mplcursors.cursor(highlight=True).\
        connect("add", lambda sel:
                sel.annotation.set_text(sel.artist.get_label()))
    plt.tight_layout()
    plt.show()


def plot_series(series: list, title=None, legend=None,
                y_percent=False, x_hour=False, y_label=None, x_label=None,
                grid=False, marker=None):
    '''
    Plot list of series

    Parameters
    ----------
    series : list
        List of pandas series.
    title : TYPE, optional
        Name of plot. The default is None.
    legend : TYPE, optional
        list of labels. The default is None.
    y_percent : TYPE, optional
        PLot 0 to 100. The default is False.
    x_hour : TYPE, optional
        plot 0 to 24. The default is False.
    y_label : str, optional
        label for y axis. The default is None.
    x_label : str, optional
        label for x axis. The default is None.
    grid : bool, optional
        plot grid. The default is False.
    marker : list, optional
        plot marker. The default is None.

    '''

    count = 0
    fig, ax = plt.subplots()
    for serie in series:
        ax.plot(serie, marker=marker[count])
        count += 1

    # Set title
    if title:
        ax.set_title(title, fontsize=24)

    # Set legend
    if legend:
        plt.legend(legend)

    # Set yticks abd xticks
    if y_percent:
        plt.yticks(np.arange(0, 101, step=10))
    if x_hour:
        plt.xticks(np.arange(0, 25, step=1))

    # Set y and x label
    if y_label:
        plt.ylabel('Porcentaje %')
    if x_label:
        plt.xlabel('Hour of the day')

    # Set grid
    if grid:
        plt.grid()

    plt.tight_layout()
    plt.show()
