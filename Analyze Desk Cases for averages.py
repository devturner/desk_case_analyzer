import os
import re
import csv
import pandas as pd
from pandas.tseries.offsets import *
import datetime
import numpy as np
import collections

# This will brute-force the results we need. 
# Change the output filename to this month
# Change the file location to this months desk report csv file


file_of_cases = "case-export-1485972653-175403.csv"

save_this_months_results = "Jan_results.csv"

df = pd.read_csv(file_of_cases)


# remove unneeded columns
df=df.drop(df.columns[[2,3,4,5,6,7,8,9,10,11,12,13,18,19,20,25,27,28,29,30,31,32,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141]], axis=1)

# Time the case was created
start = pd.to_datetime(pd.Series(df['Created At']))

# Time case was first responded to
end = pd.to_datetime(pd.Series(df['Time of First Response']))

# Add this column
df['Calculated Time to First Response'] = end - start

# Average with all cases
mean1 = df['Calculated Time to First Response'].mean()
df['Average All Cases'] = mean1

# make the created time the df index in pandas datetime
df.index = pd.to_datetime(pd.Series(df['Created At']))

# remove anything labeled afterhours
df = df[df.Labels.str.contains("Afterhours") ==False]


# remove non-business hours by day and hour

df['Day_of_week'] = df.index.weekday_name
df = df[df.Day_of_week.str.contains("Sunday") ==False]
df = df[df.Day_of_week.str.contains("Saturday") ==False]



df['time_of_day'] = df.index.hour

df = df.drop(df[df.index.hour > 18].index)
df = df.drop(df[df.index.hour < 6].index)

mean2 = df['Calculated Time to First Response'].mean()
df['Average Work Hours Cases'] = mean2

print "All cases ", mean1
print "Business cases ", mean2

df.to_csv(save_this_months_results)



