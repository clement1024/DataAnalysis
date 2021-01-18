import os.path

import plotly.graph_objs as go
import pandas as pd

import numpy as np

# import matplotlib.pyplot as plt
import math

# float value precision
pd.options.display.float_format = '{:,.2f}'.format
# base path for product list csv file
BASE_DIR = 'C:\\Users\\Clement\\Desktop\\jose_company\\';

# open csv
print('Detection MTBF for each company_id, asset_id and scenario_id')
company_data = pd.read_csv(os.path.join(BASE_DIR, "sample_data.csv"), encoding = "latin")

mtbf_data = company_data[company_data['detection_outcome']=='Not Detected'].groupby(["company_id", "asset_id", "scenario_id"])['detection_outcome'].count()
dic = mtbf_data.to_dict()
dic_keys = list(dic.keys())
dic_values = list(dic.values())
company_ids = []
asset_ids = []
scenario_ids = []
for i in range(len(dic_values)):
    company_ids.append(dic_keys[i][0])
    asset_ids.append(dic_keys[i][1])
    scenario_ids.append(dic_keys[i][2])
    dic_values[i] = round(2160.0/dic_values[i])
mtbf1 = {'company_id': company_ids, 'asset_id': asset_ids, 'scenario_id': scenario_ids, 'mtbf': dic_values}
df = pd.DataFrame(mtbf1)
fig = go.Figure(data=[go.Table(
    header=dict(values=["company_id", "asset_id", "scenario_id", "MTBF"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.company_id, df.asset_id, df.scenario_id, df.mtbf],
               fill_color='lavender',
               align='left'))
])
fig.show()

print('Detection MTBF for each company_id and asset_id')
mtbf_data = company_data[company_data['detection_outcome']=='Not Detected'].groupby(["company_id", "asset_id"])['detection_outcome'].count()
dic = mtbf_data.to_dict()
dic_keys = list(dic.keys())
dic_values = list(dic.values())
company_ids = []
asset_ids = []
for i in range(len(dic_values)):
    company_ids.append(dic_keys[i][0])
    asset_ids.append(dic_keys[i][1])
    dic_values[i] = round(2160.0/dic_values[i])
mtbf1 = {'company_id': company_ids, 'asset_id': asset_ids, 'mtbf': dic_values}
df = pd.DataFrame(mtbf1)
fig = go.Figure(data=[go.Table(
    header=dict(values=["company_id", "asset_id", "MTBF"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.company_id, df.asset_id, df.mtbf],
               fill_color='lavender',
               align='left'))
])
fig.show()

print('Detection MTBF for each company_id')
mtbf_data = company_data[company_data['detection_outcome']=='Not Detected'].groupby(["company_id"])['detection_outcome'].count()
dic = mtbf_data.to_dict()
dic_keys = list(dic.keys())
dic_values = list(dic.values())
company_ids = []
for i in range(len(dic_values)):
    company_ids.append(dic_keys[i])
    dic_values[i] = round(2160.0/dic_values[i])
mtbf1 = {'company_id': company_ids, 'mtbf': dic_values}
df = pd.DataFrame(mtbf1)
fig = go.Figure(data=[go.Table(
    header=dict(values=["company_id", "MTBF"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.company_id, df.mtbf],
               fill_color='lavender',
               align='left'))
])
fig.show()

print('Detection MTBF for each industry')
mtbf_data = company_data[company_data['detection_outcome']=='Not Detected'].groupby(["industry"])['detection_outcome'].count()
dic = mtbf_data.to_dict()
dic_keys = list(dic.keys())
dic_values = list(dic.values())
industries = []
for i in range(len(dic_values)):
    industries.append(dic_keys[i])
    dic_values[i] = round(2160.0/dic_values[i])
mtbf1 = {'industry': industries, 'mtbf': dic_values}
df = pd.DataFrame(mtbf1)
fig = go.Figure(data=[go.Table(
    header=dict(values=["industry", "MTBF"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.industry, df.mtbf],
               fill_color='lavender',
               align='left'))
])
fig.show()

company_data_to_join_left = company_data[company_data['detection_outcome']=='Not Detected']
company_data_to_join_right = company_data[company_data['detection_outcome']=='Detected']

joined_company_data = pd.merge(company_data_to_join_left, company_data_to_join_right, how='inner', left_on=['company_id', 'asset_id', 'scenario_id', 'industry'], right_on = ['company_id', 'asset_id', 'scenario_id', 'industry'])
joined_company_data['created_x'] = joined_company_data['created_x'].astype('datetime64[ns]')
joined_company_data['created_y'] = joined_company_data['created_y'].astype('datetime64[ns]')
joined_company_data = joined_company_data[joined_company_data['created_x']<joined_company_data['created_y']]

joined_company_data = joined_company_data.filter(items=['created_x', 'created_y', 'company_id', 'asset_id', 'scenario_id', 'industry'])

joined_company_data.columns = ['Not Detected_created', 'Detected_created', 'company_id', 'asset_id', 'scenario_id', 'industry']

joined_company_data = joined_company_data.sort_values(by=['Not Detected_created', 'Detected_created']);
joined_company_data1 = joined_company_data.groupby(['Not Detected_created', 'company_id', 'asset_id', 'scenario_id', 'industry'])['Detected_created'];
joined_company_data['min_Detected_created' ] = joined_company_data1.transform('min')

joined_company_data = joined_company_data.drop(columns=['Detected_created',])
joined_company_data = joined_company_data.drop_duplicates()
joined_company_data = joined_company_data.rename(columns={"min_Detected_created": "Detected_created"})

joined_company_data['date_diff_by_hours'] = joined_company_data['Detected_created'] - joined_company_data['Not Detected_created']
joined_company_data['date_diff_by_hours'] = joined_company_data['date_diff_by_hours']/np.timedelta64(1,'h')

print('Detection MTTR for each company_id, asset_id and scenario_id')

joined_company_data1 = joined_company_data.copy()
joined_company_data2 = joined_company_data.groupby(['company_id', 'asset_id', 'scenario_id'])['date_diff_by_hours'];
joined_company_data1['mttr'] = round(joined_company_data2.transform('mean'))
joined_company_data1 = joined_company_data1.drop(columns=['Not Detected_created', 'Detected_created', 'date_diff_by_hours', 'industry'])
joined_company_data1 = joined_company_data1.drop_duplicates()

# print(len(joined_company_data.index))
fig = go.Figure(data=[go.Table(
    header=dict(values=["company_id", "asset_id", "scenario_id", "MTTR"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[joined_company_data1.company_id, joined_company_data1.asset_id, joined_company_data1.scenario_id, joined_company_data1.mttr],
               fill_color='lavender',
               align='left'))
])
fig.show()

print('Detection MTTR for each company_id and asset_id')

joined_company_data1 = joined_company_data.copy()
joined_company_data2 = joined_company_data1.groupby(['company_id', 'asset_id'])['date_diff_by_hours'];
joined_company_data1['mttr'] = round(joined_company_data2.transform('mean'))
joined_company_data1 = joined_company_data1.drop(columns=['Not Detected_created', 'Detected_created', 'scenario_id', 'date_diff_by_hours', 'industry'])
joined_company_data1 = joined_company_data1.drop_duplicates()

# print(len(joined_company_data.index))
fig = go.Figure(data=[go.Table(
    header=dict(values=["company_id", "asset_id", "MTTR"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[joined_company_data1.company_id, joined_company_data1.asset_id, joined_company_data1.mttr],
               fill_color='lavender',
               align='left'))
])
fig.show()
fig.show()

print('Detection MTTR for each company_id')

joined_company_data1 = joined_company_data.copy()
joined_company_data2 = joined_company_data1.groupby(['company_id'])['date_diff_by_hours'];
joined_company_data1['mttr'] = round(joined_company_data2.transform('mean'))
joined_company_data1 = joined_company_data1.drop(columns=['Not Detected_created', 'Detected_created', 'asset_id', 'scenario_id', 'date_diff_by_hours', 'industry'])
joined_company_data1 = joined_company_data1.drop_duplicates()

# print(len(joined_company_data.index))
fig = go.Figure(data=[go.Table(
    header=dict(values=["company_id", "MTTR"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[joined_company_data1.company_id, joined_company_data1.mttr],
               fill_color='lavender',
               align='left'))
])
fig.show()

print('Detection MTTR for each industry')

joined_company_data1 = joined_company_data.copy()
joined_company_data2 = joined_company_data1.groupby(['industry'])['date_diff_by_hours'];
joined_company_data1['mttr'] = round(joined_company_data2.transform('mean'))
joined_company_data1 = joined_company_data1.drop(columns=['Not Detected_created', 'Detected_created', 'company_id', 'asset_id', 'scenario_id', 'date_diff_by_hours'])
joined_company_data1 = joined_company_data1.drop_duplicates()

# print(len(joined_company_data.index))
fig = go.Figure(data=[go.Table(
    header=dict(values=["industry", "MTTR"],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[joined_company_data1.industry, joined_company_data1.mttr],
               fill_color='lavender',
               align='left'))
])
fig.show()