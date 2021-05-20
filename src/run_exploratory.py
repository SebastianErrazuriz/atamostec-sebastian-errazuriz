import pandas as pd
from src.utils.read_files import read_txt_file
from src.utils.plots import (plot_irradiance, plot_temp, plot_watt,
                             plot_sensor, plot_clusters, plot_series)
from src.utils.sensors import (sensor_count, sensor_front_rear)
from src.utils.PR_calculation import (pr_corr, pr)
from src.utils.data_cleaning import (mean_by_hour, low_watt)
import matplotlib.pyplot as plt
import numpy as np


# Read txt files
df_ACPNorth = read_txt_file('2021-05-08_Data/CDAQ/20210508_ACpowerNorth.txt')
df_ACPSouth = read_txt_file('2021-05-08_Data/CDAQ/20210508_ACpowerSouth.txt')
df_DCPNorth = read_txt_file('2021-05-08_Data/CDAQ/20210508_DCpowerNorth.txt')
df_DCPSouth = read_txt_file('2021-05-08_Data/CDAQ/20210508_DCpowerSouth.txt')
df_MiniModules =\
    read_txt_file('2021-05-08_Data/CDAQ/20210508_MiniModules.txt')
df_RCellFixed =\
    read_txt_file('2021-05-08_Data/CDAQ/20210508_RefCellsFixed.txt')
df_RCellHSAT = read_txt_file('2021-05-08_Data/CDAQ/20210508_RefCellsHSAT.txt')
df_RCellVert = read_txt_file('2021-05-08_Data/CDAQ/20210508_RefCellsVert.txt')
df_TModFixed = read_txt_file('2021-05-08_Data/CDAQ/20210508_TempModFixed.txt')
df_TModHSAT = read_txt_file('2021-05-08_Data/CDAQ/20210508_TempModHSAT.txt')
df_TModVert = read_txt_file('2021-05-08_Data/CDAQ/20210508_TempModVert.txt')
df_WFixed = read_txt_file('2021-05-08_Data/CDAQ/20210508_WindFixed.txt')
df_WHSAT = read_txt_file('2021-05-08_Data/CDAQ/20210508_WindHSAT.txt')
df_WVertical = read_txt_file('2021-05-08_Data/CDAQ/20210508_WindVertical.txt')


# rolling mean DC (Energy output)
df_DCPSouth = df_DCPSouth.rolling(10).median()
df_DCPNorth = df_DCPNorth.rolling(10).median()

# defining Energy output in AC, after inversor
df_ACPNorth['watt1(W)'] = df_ACPNorth['VoltageInvert1(V)'] *\
                        df_ACPNorth['CurrentInvert1(A)']
df_ACPNorth['watt2(W)'] = df_ACPNorth['VoltageInvert2(V)'] *\
                        df_ACPNorth['CurrentInvert2(A)']

df_ACPSouth['watt3(W)'] = df_ACPSouth['VoltageInvert3(V)'] *\
                        df_ACPSouth['CurrentInvert3(A)']
df_ACPSouth['watt4(W)'] = df_ACPSouth['VoltageInvert4(V)'] *\
                        df_ACPSouth['CurrentInvert4(A)']
df_ACPSouth['watt5(W)'] = df_ACPSouth['VoltageInvert5(V)'] *\
                        df_ACPSouth['CurrentInvert5(A)']
df_ACPSouth['watt6(W)'] = df_ACPSouth['VoltageInvert6(V)'] *\
                        df_ACPSouth['CurrentInvert6(A)']

# Eliminate (w) under 40 considered residual
# Set watts to zero after 21:56:55
watts_north = ['watt1(W)', 'watt2(W)']
watts_south = ['watt3(W)', 'watt4(W)', 'watt5(W)', 'watt6(W)']
for watts_col in watts_south:
    df_ACPSouth[watts_col] = df_ACPSouth.\
        apply(lambda x: low_watt(x[watts_col], umbral=40), axis=1)
    df_ACPSouth.loc['2021-05-08 21:56:55':, watts_col] = 0
for watts_col in watts_north:
    df_ACPNorth[watts_col] = df_ACPNorth.\
        apply(lambda x: low_watt(x[watts_col], umbral=40), axis=1)
    df_ACPNorth.loc['2021-05-08 21:56:55':, watts_col] = 0

# rolling mean AC (Energy output)
df_ACPSouth = df_ACPSouth.rolling(10).median()
df_ACPNorth = df_ACPNorth.rolling(10).median()

# Plot AC watt
df_ACPNorth['watt1(W)'].plot()
df_ACPNorth['watt2(W)'].plot()
df_ACPSouth['watt3(W)'].plot()
df_ACPSouth['watt4(W)'].plot()
df_ACPSouth['watt5(W)'].plot()
df_ACPSouth['watt6(W)'].plot()

# Mean temperature
df_TModFixed = df_TModFixed.drop(columns=['1TE420(C)']).mean(axis=1)
df_TModHSAT = df_TModHSAT.drop(columns=['1TE601(C)']).mean(axis=1)
df_TModVert = df_TModVert.mean(axis=1)

# Plot grouped temperatures
plot_series([df_TModFixed], 'Temperatura Bifacial fixed (C)')
plot_series([df_TModHSAT], 'Temperatura Bifacial HSAT (C)')
plot_series([df_TModVert], 'Temperatura Bifacial vertical (C)')
##############################################################################
# To plot outside spyder use
# %matplotlib qt
plot_irradiance(
    df_RCellFixed, title='Irradiancia Bifacial HSAT (wm^2)')
plot_temp(df_TModFixed, title='Temperatura Bifacial fixed (C)')
plot_sensor(df_RCellHSAT, '1RC608')
plot_watt(df_ACPNorth, title='Potencias AC contenedor sur (W)')

# sensor count To use outside spyder
[count, sensors] = sensor_count(df_TModFixed)
print('Number of sensors : {}'.fotmat(count))
print('List of sensors : {}'.format(sensors))

# ['2021-05-08 20:30:00', '2021-05-08 21:00:00'] pm
# sensors classification To use outside spyder
dic = sensor_front_rear(df_MiniModules)
print('front sensors : {}'.format(dic['front']))
print('rear sensors : {}'.format(dic['rear']))

##############################################################################

# no se consideran los sensores
# c1: front
# c2: rear
# 1RC405(w.m-2) nulo
df_RCellFixed_clusters = {'c1': ['1RC410(w.m-2)', '1RC412(w.m-2)',
                                 '1RC411(w.m-2)'],
                          'c2': ['1RC407(w.m-2)', '1RC404(w.m-2)',
                                 '1RC401(w.m-2)', '1RC402(w.m-2)',
                                 '1RC408(w.m-2)',
                                 '1RC403(w.m-2)', '1RC409(w.m-2)',
                                 '1RC406(w.m-2)']}

# no se consideran los sensores
# c1: front
# 1RC605(w.m-2) ruido
# c2: rear
df_RCellHSAT_clusters = {'c1': ['1RC607(w.m-2)', '1RC609(w.m-2)'],
                         'c2': ['1RC603(w.m-2)', '1RC601(w.m-2)',
                                '1RC612(w.m-2)', '1RC604(w.m-2)',
                                '1RC610(w.m-2)', '1RC602(w.m-2)',
                                '1RC611(w.m-2)', '1RC606(w.m-2)',
                                '1RC608(w.m-2)']}

# no se consideran los sensores
# c1 AM: sensores que miran hacia el este
# 1RC102(w.m-2) ruido
# c2 PM: sensores que miran hacia el oeste
# 1RC110(w.m-2) ruido
df_RCellVert_clusters = {'c1': ['1RC113(w.m-2)', '1RC109(w.m-2)',
                                '1RC107(w.m-2)', '1RC121(w.m-2)',
                                '1RC108(w.m-2)', '1RC119(w.m-2)',
                                '1RC103(w.m-2)', '1RC101(w.m-2)',
                                '1RC114(w.m-2)', '1RC115(w.m-2)',
                                '1RC120(w.m-2)'],
                         'c2': ['1RC112(w.m-2)', '1RC124(w.m-2)',
                                '1RC106(w.m-2)', '1RC122(w.m-2)',
                                '1RC117(w.m-2)', '1RC105(w.m-2)',
                                '1RC118(w.m-2)', '1RC104(w.m-2)',
                                '1RC116(w.m-2)', '1RC110(w.m-2)',
                                '1RC111(w.m-2)', '1RC123(w.m-2)']}

# calculate the mean for each technology
for cluster in df_RCellFixed_clusters.keys():
    df_RCellFixed[cluster] =\
        df_RCellFixed[df_RCellFixed_clusters[cluster]].mean(axis=1)

for cluster in df_RCellHSAT_clusters.keys():
    df_RCellHSAT[cluster] =\
        df_RCellHSAT[df_RCellHSAT_clusters[cluster]].mean(axis=1)

for cluster in df_RCellVert_clusters.keys():
    df_RCellVert[cluster] =\
        df_RCellVert[df_RCellVert_clusters[cluster]].mean(axis=1)

# PLot the irradiance clusters
plot_clusters(df_RCellFixed, title='Irradiancia Bifacial fixed (wm^2)')
plot_clusters(df_RCellHSAT, title='Irradiancia Bifacial HSAT (wm^2)')
plot_clusters(df_RCellVert, title='Irradiancia Bifacial vetical (wm^2)')

##############################################################################
# Irradiance
# FIXED
# the front and rear sum
i_sum_fixed = df_RCellFixed['c1'] + df_RCellFixed['c2']
i_sum_fixed = pd.DataFrame(i_sum_fixed, columns=["SUM IRR Fixed"])

# only the front
i_front_fixed = df_RCellFixed[['c1']]
i_front_fixed.columns = ["FRONT IRR Fixed"]

# HSAT
# the front and rear sum
i_sum_hsat = df_RCellHSAT['c1'] + df_RCellHSAT['c2']
i_sum_hsat = pd.DataFrame(i_sum_hsat, columns=["SUM IRR HSAT"])

# only the front
i_front_hsat = df_RCellHSAT[['c1']]
i_front_hsat.columns = ["FRONT IRR HSAT"]

# VERT
# the front and rear sum (west and east)
i_sum_vert = df_RCellVert['c1'] + df_RCellVert['c2']
i_sum_vert = pd.DataFrame(i_sum_vert, columns=["SUM IRR Vert"])

# plot irrandiance
plot_series([i_sum_fixed, i_sum_hsat, i_sum_vert],
            title='Irradiancias de los tres sistemas (w.m-2)',
            legend=['Irradiancia en fized', 'Irradiancia en HSAT',
            'Irradiancia en vertical'])

# FIXED #######################################################################

t_avg_fixed = pd.DataFrame(df_TModFixed, columns=["AVG Temp Fixed"])
t_avg_fixed.reset_index(drop=False, inplace=True)

# suma de temperaturas fixed
w_sum_fixed = df_DCPSouth[["1PE501(W)", "1PE503(W)",
                           "1PE502(W)", "1PE504(W)"]].sum(axis=1)
w_sum_fixed = pd.DataFrame(w_sum_fixed, columns=["SUM W Fixed"])

w_avg_fixed = df_DCPSouth[["1PE501(W)", "1PE503(W)",
                           "1PE502(W)", "1PE504(W)"]].mean(axis=1)
w_avg_fixed = pd.DataFrame(w_avg_fixed, columns=["AVG W Fixed"])

# Join power DC with irradiance, avarage power and frontal irradiance
data_dc_fix = w_sum_fixed.merge(t_avg_fixed, on=["TimeStamp"], how="outer")
data_dc_fix = data_dc_fix.merge(i_sum_fixed, on=["TimeStamp"], how="outer")
data_dc_fix = data_dc_fix.merge(w_avg_fixed, on=["TimeStamp"], how="outer")
data_dc_fix = data_dc_fix.merge(i_front_fixed, on=["TimeStamp"], how="outer")

# compute performance
data_dc_fix["PR_W_IRR_SUM_FIXED"] = data_dc_fix.apply(
    lambda x: pr(x['SUM W Fixed'], x['SUM IRR Fixed'],
                 p0=450, modules=4), axis=1)
data_dc_fix["PR_CORRECTED_W_IRR_SUM_FIXED"] = data_dc_fix.apply(
    lambda x: pr_corr(x['SUM W Fixed'], x['SUM IRR Fixed'],
                      x['AVG Temp Fixed'], p0=450, modules=4), axis=1)

# Set hour resolution
data_dc_fix = mean_by_hour(data_dc_fix)

# compute values per hour
# data_dc_fix = mean_by_hour(data_dc_fix)

'''
# explore different outcomes and data_dc_fix understanding
data_dc_fix["PR_W_AVG_IRR_SUM_FIXED"] = data_dc_fix.apply(
    lambda x: pr(x['AVG W Fixed'], x['SUM IRR Fixed'], p0=450), axis=1)
data_dc_fix["PR_W_IRR_AVG_FIXED"] = data_dc_fix.apply(
    lambda x: pr(x['AVG W Fixed'], x['FRONT IRR Fixed'], p0=450), axis=1)
'''
'''
# set index as TimeStamp
data_dc_fix = data_dc_fix.set_index('TimeStamp')
'''


# HSAT ########################################################################

t_avg_hsat = pd.DataFrame(df_TModHSAT, columns=["AVG Temp HSAT"])
t_avg_hsat.reset_index(drop=False, inplace=True)

# suma de temperaturas HSAT
w_sum_hsat = df_DCPSouth[["1PE505(W)", "1PE508(W)",
                          "1PE506(W)", "1PE507(W)"]].sum(axis=1)
w_sum_hsat = pd.DataFrame(w_sum_hsat, columns=["SUM W HSAT"])

w_avg_hsat = df_DCPSouth[["1PE505(W)", "1PE508(W)",
                          "1PE506(W)", "1PE507(W)"]].mean(axis=1)
w_avg_hsat = pd.DataFrame(w_avg_hsat, columns=["AVG W HSAT"])


data_dc_hsat = w_sum_hsat.merge(t_avg_hsat, on=["TimeStamp"], how="outer")
data_dc_hsat = data_dc_hsat.merge(i_sum_hsat, on=["TimeStamp"], how="outer")
data_dc_hsat = data_dc_hsat.merge(w_avg_hsat, on=["TimeStamp"], how="outer")
data_dc_hsat = data_dc_hsat.merge(i_front_hsat, on=["TimeStamp"], how="outer")


data_dc_hsat["PR_W_IRR_SUM_HSAT"] = data_dc_hsat.apply(
    lambda x: pr(x['SUM W HSAT'], x['SUM IRR HSAT'],
                 p0=450, modules=4), axis=1)
data_dc_hsat["PR_CORRECTED_W_IRR_SUM_HSAT"] = data_dc_hsat.apply(
    lambda x: pr_corr(x['SUM W HSAT'], x['SUM IRR HSAT'],
                      x['AVG Temp HSAT'], p0=450, modules=4), axis=1)

# Set hour resolution
data_dc_hsat = mean_by_hour(data_dc_hsat)

# set index as TimeStamp
# data_dc_hsat = data_dc_hsat.set_index('TimeStamp')

# VERTICAL ###################################################################

t_avg_vert = pd.DataFrame(df_TModVert, columns=["AVG Temp Vert"])
t_avg_vert.reset_index(drop=False, inplace=True)

# suma de temperaturas vert
w_sum_vert = df_DCPNorth[["1PE301(W)", "1PE302(W)", "1PE303(W)"]].sum(axis=1)
w_sum_vert = pd.DataFrame(w_sum_vert, columns=["SUM W Vert"])

w_avg_vert = df_DCPNorth[["1PE301(W)", "1PE302(W)", "1PE303(W)"]].mean(axis=1)
w_avg_vert = pd.DataFrame(w_avg_vert, columns=["AVG W Vert"])


data_dc_vert = w_sum_vert.merge(t_avg_vert, on=["TimeStamp"], how="outer")
data_dc_vert = data_dc_vert.merge(i_sum_vert, on=["TimeStamp"], how="outer")
data_dc_vert = data_dc_vert.merge(w_avg_vert, on=["TimeStamp"], how="outer")

data_dc_vert["PR_W_IRR_SUM_vert"] = data_dc_vert.apply(
    lambda x: pr(x['SUM W Vert'], x['SUM IRR Vert'],
                 p0=450, modules=3), axis=1)
data_dc_vert["PR_CORRECTED_W_IRR_SUM_vert"] = data_dc_vert.apply(
    lambda x: pr_corr(x['SUM W Vert'], x['SUM IRR Vert'],
                      x['AVG Temp Vert'], p0=450, modules=3), axis=1)

# Set hour resolution
data_dc_vert = mean_by_hour(data_dc_vert)

# set index as TimeStamp
# data_dc_vert = data_dc_vert.set_index('TimeStamp')

###############################################################################
# AC POWER ####################################################################

# FIXED #######################################################################
t_avg_fixed = pd.DataFrame(df_TModFixed, columns=["AVG Temp Fixed"])
t_avg_fixed.reset_index(drop=False, inplace=True)

# suma de temperaturas fixed
w_sum_fixed_ac = df_ACPSouth[["watt3(W)", "watt4(W)"]].sum(axis=1)
w_sum_fixed_ac = pd.DataFrame(w_sum_fixed_ac, columns=["SUM W Fixed_ac"])

w_avg_fixed_ac = df_ACPSouth[["watt3(W)", "watt4(W)"]].mean(axis=1)
w_avg_fixed_ac = pd.DataFrame(w_avg_fixed_ac, columns=["AVG W Fixed_ac"])


data_ac_fix = w_sum_fixed_ac.merge(t_avg_fixed, on=["TimeStamp"], how="outer")
data_ac_fix = data_ac_fix.merge(i_sum_fixed, on=["TimeStamp"], how="outer")
data_ac_fix = data_ac_fix.merge(w_avg_fixed_ac, on=["TimeStamp"], how="outer")
data_ac_fix = data_ac_fix.merge(i_front_fixed, on=["TimeStamp"], how="outer")


data_ac_fix["PR_W_IRR_SUM_FIXED_ac"] = data_ac_fix.apply(
    lambda x: pr(x['SUM W Fixed_ac'], x['SUM IRR Fixed'],
                 p0=450, modules=4), axis=1)
data_ac_fix["PR_CORRECTED_W_IRR_SUM_FIXED_ac"] = data_ac_fix.apply(
    lambda x: pr_corr(x['SUM W Fixed_ac'], x['SUM IRR Fixed'],
                      x['AVG Temp Fixed'], p0=450, modules=4), axis=1)

# Set hour resolution
data_ac_fix = mean_by_hour(data_ac_fix)


# set index as TimeStamp
# data_ac_fix = data.set_index('TimeStamp')

# HSAT ########################################################################
t_avg_hsat = pd.DataFrame(df_TModHSAT, columns=["AVG Temp HSAT"])
t_avg_hsat.reset_index(drop=False, inplace=True)

# suma de temperaturas fixed
w_sum_hsat_ac = df_ACPSouth[["watt5(W)", "watt5(W)"]].sum(axis=1)
w_sum_hsat_ac = pd.DataFrame(w_sum_hsat_ac, columns=["SUM W HSAT_ac"])

w_avg_hsat_ac = df_ACPSouth[["watt5(W)", "watt6(W)"]].mean(axis=1)
w_avg_hsat_ac = pd.DataFrame(w_avg_hsat_ac, columns=["AVG W HSAT_ac"])


data_ac_hsat = w_sum_hsat_ac.merge(t_avg_hsat, on=["TimeStamp"], how="outer")
data_ac_hsat = data_ac_hsat.merge(i_sum_hsat, on=["TimeStamp"], how="outer")
data_ac_hsat = data_ac_hsat.merge(w_avg_hsat_ac, on=["TimeStamp"], how="outer")
data_ac_hsat = data_ac_hsat.merge(i_front_hsat, on=["TimeStamp"], how="outer")


data_ac_hsat["PR_W_IRR_SUM_HSAT_ac"] = data_ac_hsat.apply(
    lambda x: pr(x['SUM W HSAT_ac'], x['SUM IRR HSAT'],
                 p0=450, modules=4), axis=1)
data_ac_hsat["PR_CORRECTED_W_IRR_SUM_HSAT_ac"] = data_ac_hsat.apply(
    lambda x: pr_corr(x['SUM W HSAT_ac'], x['SUM IRR HSAT'],
                      x['AVG Temp HSAT'], p0=450, modules=4), axis=1)

data_ac_hsat = mean_by_hour(data_ac_hsat)

# set index as TimeStamp
# data_ac_hsat = data.set_index('TimeStamp')

# VERTICAL ####################################################################
t_avg_vert = pd.DataFrame(df_TModVert, columns=["AVG Temp Vert"])
t_avg_vert.reset_index(drop=False, inplace=True)

# suma de temperaturas fixed
w_sum_vert_ac = df_ACPNorth[["watt1(W)", "watt2(W)"]].sum(axis=1)
w_sum_vert_ac = pd.DataFrame(w_sum_vert_ac, columns=["SUM W Vert_ac"])

w_avg_vert_ac = df_ACPNorth[["watt1(W)", "watt2(W)"]].mean(axis=1)
w_avg_vert_ac = pd.DataFrame(w_avg_vert_ac, columns=["AVG W Vert_ac"])


data_ac_vert = w_sum_vert_ac.merge(t_avg_vert, on=["TimeStamp"], how="outer")
data_ac_vert = data_ac_vert.merge(i_sum_vert, on=["TimeStamp"], how="outer")
data_ac_vert = data_ac_vert.merge(w_avg_vert_ac, on=["TimeStamp"], how="outer")


data_ac_vert["PR_W_IRR_SUM_Vert_ac"] = data_ac_vert.apply(
    lambda x: pr(x['SUM W Vert_ac'], x['SUM IRR Vert'],
                 p0=450, modules=3), axis=1)
data_ac_vert["PR_CORRECTED_W_IRR_SUM_Vert_ac"] = data_ac_vert.apply(
    lambda x: pr_corr(x['SUM W Vert_ac'], x['SUM IRR Vert'],
                      x['AVG Temp Vert'], p0=450, modules=3), axis=1)

data_ac_vert = mean_by_hour(data_ac_vert)

# set index as TimeStamp
# data_ac_vert = data.set_index('TimeStamp')

##############################################################################
##############################################################################
'''
We use data_dc_[fix, hsat, vert] and data_ac_[fix, hsat, vert] for
plotting the differents dataframes series
'''

# Plot AC watt SUM
plot_series([w_sum_vert_ac, w_sum_fixed_ac, w_sum_hsat_ac],
            title='Potencia AC (w)',
            legend=['Potencia bifacial vertical', 'Potencia bifacial fixed',
                    'Potencia bifacial HSAT'])

# Plot Performance Ratio

# statistic from 11am to 21pm
# Bifacial fixed
print(data_ac_fix.loc[11: 21]["PR_W_IRR_SUM_FIXED_ac"].describe())
print(data_ac_fix.loc[11: 21]["PR_CORRECTED_W_IRR_SUM_FIXED_ac"].describe())
print(data_ac_fix.loc[11: 21]["PR_W_IRR_SUM_FIXED_ac"].median())
print(data_ac_fix.loc[11: 21]["PR_CORRECTED_W_IRR_SUM_FIXED_ac"].median())

# Bifacial HSAT
print(data_ac_hsat.loc[11: 21]["PR_W_IRR_SUM_HSAT_ac"].describe())
print(data_ac_hsat.loc[11: 21]["PR_CORRECTED_W_IRR_SUM_HSAT_ac"].describe())
print(data_ac_hsat.loc[11: 21]["PR_W_IRR_SUM_HSAT_ac"].median())
print(data_ac_hsat.loc[11: 21]["PR_CORRECTED_W_IRR_SUM_HSAT_ac"].median())

# Bifacial vert
print(data_ac_vert.loc[11: 21]["PR_W_IRR_SUM_Vert_ac"].describe())
print(data_ac_vert.loc[11: 21]["PR_CORRECTED_W_IRR_SUM_Vert_ac"].describe())
print(data_ac_vert.loc[11: 21]["PR_W_IRR_SUM_Vert_ac"].median())
print(data_ac_vert.loc[11: 21]["PR_CORRECTED_W_IRR_SUM_Vert_ac"].median())

# PR Corrected in DC and / DC
plot_series([data_dc_fix["PR_CORRECTED_W_IRR_SUM_FIXED"],
             data_ac_fix["PR_CORRECTED_W_IRR_SUM_FIXED_ac"]],
            title='PR Bifacial fixed',
            legend=['PR corregido considerando DC',
                    'PR corregido considerando AC'],
            y_percent=True,
            x_hour=True,
            y_label='Porcentaje %',
            x_label='hr del día',
            grid=True,
            marker=['.', '*'])

# PR / PR corr
# Bifacial fixed
plot_series([data_ac_fix["PR_W_IRR_SUM_FIXED_ac"],
             data_ac_fix["PR_CORRECTED_W_IRR_SUM_FIXED_ac"]],
            title='PR Bifacial fixed',
            legend=['PR', 'PR corregido'],
            y_percent=True,
            x_hour=True,
            y_label='Porcentaje %',
            x_label='hr del día',
            grid=True,
            marker=['.', '*'])

# Bifacial HSAT
plot_series([data_ac_hsat["PR_W_IRR_SUM_HSAT_ac"],
             data_ac_hsat["PR_CORRECTED_W_IRR_SUM_HSAT_ac"]],
            title='PR Bifacial HSAT',
            legend=['PR', 'PR corregido'],
            y_percent=True,
            x_hour=True,
            y_label='Porcentaje %',
            x_label='hr del día',
            grid=True,
            marker=['.', '*'])

# Bifacial vert
plot_series([data_ac_vert["PR_W_IRR_SUM_Vert_ac"],
             data_ac_vert["PR_CORRECTED_W_IRR_SUM_Vert_ac"]],
            title='PR Bifacial vertical',
            legend=['PR', 'PR corregido'],
            y_percent=True,
            x_hour=True,
            y_label='Porcentaje %',
            x_label='hr del día',
            grid=True,
            marker=['.', '*'])

# PR de los sistemas
plot_series([data_ac_fix["PR_W_IRR_SUM_FIXED_ac"],
             data_ac_hsat["PR_W_IRR_SUM_HSAT_ac"],
             data_ac_vert["PR_W_IRR_SUM_Vert_ac"]],
            title='PR de los tres sistemas',
            legend=['Bifacial fixed', 'Bifacial HSAT', 'Bifacial vertical'],
            y_percent=True,
            x_hour=True,
            y_label='Porcentaje %',
            x_label='hr del día',
            grid=True,
            marker=['.', '*', '^'])

# PR corr de los sistemas
plot_series([data_ac_fix["PR_CORRECTED_W_IRR_SUM_FIXED_ac"],
             data_ac_hsat["PR_CORRECTED_W_IRR_SUM_HSAT_ac"],
             data_ac_vert["PR_CORRECTED_W_IRR_SUM_Vert_ac"]],
            title='PR corregido de los tres sistemas',
            legend=['Bifacial fixed', 'Bifacial HSAT', 'Bifacial vertical'],
            y_percent=True,
            x_hour=True,
            y_label='Porcentaje %',
            x_label='hr del día',
            grid=True,
            marker=['.', '*', '^'])


# correlation of temp and PR
fig, ax = plt.subplots(1, 3, figsize=(10, 4), sharey=True, sharex=True)
fig.suptitle('Correlación de PR corregido vs Temperatura', fontsize=14)

ax[0].scatter(data_ac_fix.loc[12: 20]["AVG Temp Fixed"],
              data_ac_fix.loc[12: 20]["PR_CORRECTED_W_IRR_SUM_FIXED_ac"])
ax[1].scatter(data_ac_hsat.loc[12: 20]["AVG Temp HSAT"],
              data_ac_hsat.loc[12: 20]["PR_CORRECTED_W_IRR_SUM_HSAT_ac"])
ax[2].scatter(data_ac_vert.loc[12: 20]["AVG Temp Vert"],
              data_ac_vert.loc[12: 20]["PR_CORRECTED_W_IRR_SUM_Vert_ac"])

ax[0].set_title('Bifacial fixed')
ax[1].set_title('Bifacial HSAT')
ax[2].set_title('Bifacial vertical')

ax[0].set_ylabel('PR correcgido [%]')

plt.yticks(np.arange(60, 101, step=10))
plt.xticks(np.arange(20, 61, step=10))
fig.tight_layout()
plt.show()

# print correlation
print('Correlación Pearson fixed: ',
      data_ac_fix.loc[12: 20]["AVG Temp Fixed"].corr(
          data_ac_fix.loc[12: 20]["PR_CORRECTED_W_IRR_SUM_FIXED_ac"],
          method='pearson'))

print('Correlación Pearson HSAT: ',
      data_ac_hsat.loc[12: 20]["AVG Temp HSAT"].corr(
          data_ac_hsat.loc[12: 20]["PR_CORRECTED_W_IRR_SUM_HSAT_ac"],
          method='pearson'))


print('Correlación Pearson vertical: ',
      data_ac_vert.loc[12: 20]["AVG Temp Vert"].corr(
          data_ac_vert.loc[12: 20]["PR_CORRECTED_W_IRR_SUM_Vert_ac"],
          method='pearson'))

# create dataframe for barplot
pr_ac_fix = pd.DataFrame(data_ac_fix.loc[11: 21],
                         columns=["PR_W_IRR_SUM_FIXED_ac"])
pr_ac_fix.reset_index(drop=False, inplace=True)

pr_ac_hsat = pd.DataFrame(data_ac_hsat.loc[11: 21],
                          columns=["PR_CORRECTED_W_IRR_SUM_HSAT_ac"])
pr_ac_vert = pd.DataFrame(data_ac_vert.loc[11: 21],
                          columns=["PR_CORRECTED_W_IRR_SUM_Vert_ac"])

# merge data
data_ac_pr = pr_ac_fix.merge(pr_ac_hsat, on=["hour"], how="outer")
data_ac_pr = data_ac_pr.merge(pr_ac_vert, on=["hour"], how="outer")
data_ac_pr = data_ac_pr.set_index('hour')

data_ac_pr.plot.bar(title='PR corregido promedio para las tres tecnologías',
                    yticks=np.arange(0, 101, 10),
                    ylabel='Porcentaje %')
