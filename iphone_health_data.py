import pandas as pd
import xmltodict
import calendar
import matplotlib.pyplot as plt

#soruce: https://medium.com/better-programming/analyze-your-icloud-health-data-with-pandas-dd5e963e902f

input_path = 'export.xml'
with open(input_path, 'r') as xml_file:
    input_data = xmltodict.parse(xml_file.read())




records_list = input_data['HealthData']['Record']

df = pd.DataFrame(records_list)

print(df.dtypes)
#Data inspection
df.columns


df['@type'].unique()


#analysis

format = '%Y-%m-%d %H:%M:%S %z'
df['@creationDate'] = pd.to_datetime(df['@creationDate'],
                                    format=format)
df['@startDate'] = pd.to_datetime(df['@startDate'],
                                  format=format)
df['@endDate'] = pd.to_datetime(df['@endDate'],
                             format=format  )

print(df.dtypes)
step_counts = df[df['@type'] == 'HKQuantityTypeIdentifierStepCount']


step_counts.loc[:, '@value'] = pd.to_numeric(
    step_counts.loc[:, '@value'])

print(step_counts.dtypes)

step_counts_by_creation = step_counts.groupby('@creationDate').sum()


#re-sizing 

print(step_counts_by_creation)
by_day = step_counts_by_creation['@value'].resample('D').sum()


by_day = step_counts_by_creation['@value'].resample('D').sum()

by_day.sort_values(ascending=False)[:10]

means_by_distinct_month = by_day.resample('M').mean()
means_by_distinct_month.sort_values(ascending=False)[:10]

by_day[(by_day.index.year == 2017) & (by_day.index.month == 6)]


means_by_month = means_by_distinct_month.groupby(
      means_by_distinct_month.index.month).mean()
means_by_month.index = list(calendar.month_name)[1:] 


#plotting 
print(means_by_month)
means_by_month.plot(kind='bar')
plt.show()



means_by_weekday = by_day.groupby(by_day.index.dayofweek).mean()
means_by_weekday.index = ['Monday', 'Tuesday',
                          'Wednesday', 'Thursday',
                          'Friday', 'Saturday',
                          'Sunday']


means_by_weekday.plot(kind='bar')
plt.show()