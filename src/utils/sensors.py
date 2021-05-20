from pandas.core.frame import DataFrame


def sensor_count(df: DataFrame):
    '''
    Count the sensors and returns a list with them

    Parameters
    ----------
    df : DataFrame
        Sensor cell dataframe.

    Return
    ------
    sensor_list : List
        Sensor list with their counts
    '''

    sensor = []

    for column in df:
        if '(C)' in column:
            sensor.append(column)

    return [len(sensor), sensor]


def sensor_front_rear(df: DataFrame, min_value=400.0, time=['', '']):
    '''
    Count the sensors and returns a list with the classification
    of rear and front sensors

    Parameters
    ----------
    df : DataFrame
        Sensor cell dataframe.
    min_value : TYPE, optional
        value umbral. The default is 400.0.
    time : TYPE, optional
        time range to classify. The default is ['', ''].

    Returns
    -------
    dict with front and rear sensors.

    '''

    front = []
    rear = []

    for column in df:
        if '(w.m-2)' in column:
            # time classification for vertical PV
            if time != ['', '']:
                df = df[(df.index > time[0]) & (df.index < time[1])]
                print(df)
                if any(df[column] > min_value):
                    front.append(column)
                elif not any(df[column] > min_value):
                    rear.append(column)
            # only value classification
            else:
                if any(df[column] > min_value):
                    front.append(column)
                elif not any(df[column] > min_value):
                    rear.append(column)

    return {'front': front,
            'rear': rear}
