#
# Simple country-based COVID-19 data analysis
# By nonet
#


import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
from datetime import datetime
import urllib2

# SOURCE DATA
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_time.csv"

# Useful variables
data = {}
counter = -1
previous_country=""


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
    if country == 'Country_Region':
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

    if not data.has_key(country):
        data[country] = ([],[],[])

    data[country][0].append(date)
    data[country][1].append(dead)
    if counter == 0:
        data[country][2].append(0)
    else :
        data[country][2].append(dead-data[country][1][counter-1])

### NOW DATA IS IN THE DICTIONARY

### PREPARE TO PLOT

# X axis : organised date format
x = [datetime.strptime(d,'%m/%d/%y').date() for d in data['France'][0]]

# Y axis (sevral)
deaths = {}
deaths_incremental = {}
deaths_start_10 = {}


# SPECIFY THE COUNTRIES YOU WANT
countries = ('France', 'Italy', 'US', 'Germany', 'Netherlands', 'China', 'Spain', 'Japan', 'United Kingdom', 'Switzerland')

# PREPARE PLOT AXIS
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%d-%m'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())


# PLOT THE DEATHS PROFILE
for country in countries :
    deaths[country] = data[country][1]

    plt.plot(x, deaths[country], label=country)
    plt.gca().yaxis.set_label_text('deaths')
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.gcf().autofmt_xdate()
plt.savefig('deaths.png',bbox_inches='tight' )
plt.clf()


# PLOT THE INCREMENTAL DEATH PROFILE
for country in countries :
    deaths_incremental[country] = data[country][2]

    plt.plot(x, deaths_incremental[country], label=country)
    plt.gca().yaxis.set_label_text('increment death')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.gcf().autofmt_xdate()
plt.savefig('increment_death.png',bbox_inches='tight' )
plt.clf()

# PLOT THE DEATH PROFILE starting on 10th dead
for country in countries :
    original_list = data[country][1]
    new_list = []
    found = False
    for index in range(0, len(original_list)):
        value = original_list[index]
        if value >= 10:
            found = True
        if found:
            new_list.append(original_list[index])

    shifted_x = list(range(len(new_list)))


    plt.plot(shifted_x, new_list, label=country)
    plt.gca().yaxis.set_label_text('deaths from 10th victim')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
    plt.yscale('log')
    plt.gcf().autofmt_xdate()
plt.savefig('death_start_10.png',bbox_inches='tight' )
plt.clf()

# FINISH
