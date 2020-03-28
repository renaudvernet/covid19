#
# Simple country-based COVID-19 data analysis
# By nonet
#


import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
from datetime import datetime
import urllib2
import sys
import copy


# SOURCE DATA
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_time.csv"

# Useful variables
data = {}
counter = -1
previous_country=""
time_limit_days = 30

plot_config = {
    'deaths' : {
        'logscale': False,
        'ytitle': 'number of deaths',
        'isdate': True
    } ,
    'deaths_incremental' : {
        'logscale': False,
        'ytitle': 'daily incremental deaths',
        'isdate': True
    } ,
    'deaths_start_10' : {
        'logscale': False,
        'ytitle': 'number of deaths since #10',
        'isdate': False
    } ,
    'deaths_start_10_normalized' : {
        'logscale': False,
        'ytitle': 'number of deaths since #10 (normalized)',
        'isdate': False
    } ,
}


# SPECIFY THE COUNTRIES YOU WANT with respective population
countries = {
    'France' : 65.27,
    'Italy' : 60.46,
    'US' : 331,
    'Germany' : 83.78,
    'Netherlands' : 17.13,
    'China' : 1439,
    'Spain' : 46.75,
    # 'Japan' : 126.48,
    # 'United Kingdom' : 67.89 ,
    # 'South Korea' : 51.27,
    'Iran': 83.99,
    'Belgium' : 11.59,
    # 'Switzerland' : 8.65,
    # 'Sweden': 10.1,
}

for plot_type in plot_config.keys() :
    data[plot_type] = {}
    for country in countries.keys() :
        data[plot_type][country] = {}
        data[plot_type][country]['x_points'] = []
        data[plot_type][country]['y_points'] = []

raw_data = {}
for country in countries.keys() :
    raw_data[country] = {}
    raw_data[country]['x_points'] = []
    raw_data[country]['y_points'] = {}
    raw_data[country]['y_points']['confirmed'] = []
    raw_data[country]['y_points']['dead']      = []


######################
#    NOW GET THE DATA
######################


# ORGANIZE DATA IN DICTIONARY
# keys are COUNTRY NAME
# values are tuple of lists ([],[],[])
# 1st list : dates
# 2nd list : number of deaths
# 3rd list : number of deaths with respect to previous day


input = urllib2.urlopen(url)
for line in input:

    fields = line.split(",")
    country = fields[0]
    if country not in countries.keys():
        continue

    if country != previous_country :
        counter = 0
        previous_country = country
    else :
        counter += 1

    if country == '"Korea':
        country = 'South Korea'
        date = fields[2]
        confirmed = int(fields[3])
        dead = int(fields[4])
        if fields[5]:
            recovered = int(fields[5])
        else:
            recovered = 0
    else :
        date = fields[1]
        confirmed = int(fields[2])
        dead = int(fields[3])
        if fields[4]:
            recovered = int(fields[4])
        else:
            recovered = 0


    raw_data[country]['x_points'].append(datetime.strptime(date,'%m/%d/%y').date())
    raw_data[country]['y_points']['confirmed'].append(confirmed)
    raw_data[country]['y_points']['dead'].append(dead)
### NOW DATA IS IN THE DICTIONARY



def assign_data(plot_type, raw_data) :

    if plot_type == 'deaths':
        for country in countries.keys():
            data[plot_type][country]['x_points'] = raw_data[country]['x_points']
            data[plot_type][country]['y_points'] = copy.copy(raw_data[country]['y_points']['dead'])
    elif plot_type == 'deaths_incremental':
        for country in countries.keys():
            data[plot_type][country]['x_points'] = raw_data[country]['x_points']
            data[plot_type][country]['y_points'] = copy.copy(raw_data[country]['y_points']['dead'])
            for index in reversed(range(0, len(data[plot_type][country]['y_points']))):
                if index == 0 :
                    data[plot_type][country]['y_points'][index] = 0
                else :
                    data[plot_type][country]['y_points'][index] = data[plot_type][country]['y_points'][index] - data[plot_type][country]['y_points'][index-1]
    elif plot_type == 'deaths_start_10' or plot_type == 'deaths_start_10_normalized':
        for country in countries.keys():
            original_list = raw_data[country]['y_points']['dead']
            new_list = []
            found = False
            for index in range(0, len(original_list)):
                value = original_list[index]
                if value >= 10:
                    found = True
                if found:
                    if plot_type == 'deaths_start_10' :
                        new_list.append(original_list[index])
                    elif plot_type == 'deaths_start_10' :
                        new_list.append(original_list[index]/countries[country])
                    else :
                        print 'error'
                        sys.exit(1)
            shifted_x = list(range(len(new_list)))

            data[plot_type][country]['x_points'] = shifted_x
            data[plot_type][country]['y_points'] = new_list
    else:
        print('ERROR : unknown plot type %s' % plot_type)
        sys.exit(1)

### PREPARE TO PLOT

for plot_type in plot_config.keys():
    # PREPARE PLOT AXIS
    assign_data(plot_type, raw_data)

    for country in countries.keys() :
        plt.plot(data[plot_type][country]['x_points'], data[plot_type][country]['y_points'] , label=country)

    plt.gca().yaxis.set_label_text(plot_config[plot_type]['ytitle'])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    if plot_config[plot_type]['logscale']: plt.yscale('log')
    if plot_config[plot_type]['isdate']:
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%d-%m'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
    plt.savefig('%s.png' % plot_type ,bbox_inches='tight' )
    plt.clf()


# FINISH
