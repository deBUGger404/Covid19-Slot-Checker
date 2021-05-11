import datetime
import json
import numpy as np
import requests
import pandas as pd
import streamlit
from copy import deepcopy


streamlit.title('Covid Vaccination Slot Availability')

@streamlit.cache  # This function will be cached
def district_wise_data():
    df = pd.read_csv("district_code.csv")
    return df


df = district_wise_data()
dicts = dict(zip( df['district name'],df['district id']))

unique_dist = list(df["district name"].unique())
unique_dist.sort()

no_days = streamlit.sidebar.slider('Select Date Range', 0, 100, 5)
dist_new = streamlit.sidebar.selectbox('Select District Name', unique_dist)
# pin_col, age_col, fee_col, avail_col = streamlit.sidebar.beta_columns(4)

dist_new_val = dicts[dist_new]
base = datetime.datetime.today()
list_date = [base + datetime.timedelta(days=day) for day in range(no_days)]
date_stamp = [x.strftime("%d-%m-%Y") for x in list_date]

streamlit.write(dist_new_val)

data1 = pd.DataFrame()
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
for date_ in date_stamp:
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(dist_new_val, date_)
    response = requests.get(URL, headers=header)
    streamlit.write(response)
    if (response.ok):
        assert 'centers' in json.loads(response.text)
        if response.json()['centers'] is not None:
            data = pd.DataFrame(response.json()['centers'])
            if len(data)>0:
                data = data.explode("sessions")
                data['min_age_limit'] = data.sessions.apply(lambda x: x['min_age_limit'])
                data['vaccine'] = data.sessions.apply(lambda x: x['vaccine'])
                data['available_capacity'] = data.sessions.apply(lambda x: x['available_capacity'])
                data['date'] = data.sessions.apply(lambda x: x['date'])
                data = data[["date", "available_capacity", "vaccine", "min_age_limit", "pincode", "name", "state_name", "district_name", "block_name", "fee_type"]]
                if data1 is not None:
                    data1 = pd.concat([data1, data])
                else:
                    data1 = deepcopy(data)
            else:
                streamlit.error("No rows in the data Extracted from the API")
    else:
        streamlit.error("Invalid response")

col_rename = {'date': 'Date','min_age_limit': 'Minimum Age Limit','available_capacity': 'Available Capacity','vaccine': 'Vaccine','pincode': 'Pincode','name': 'Hospital Name','state_name' : 'State','district_name' : 'District','block_name': 'Block Name','fee_type' : 'Fees'}

if (data1 is not None) & (len(data1)):
    data1.drop_duplicates(inplace=True)
    data1.rename(columns=col_rename, inplace=True)
    uni_pincode = data1["Pincode"].unique().tolist()
    valid_age = [18, 45]

    pincode_inp = streamlit.sidebar.selectbox('Select Pincode', [""] + uni_pincode)
    if pincode_inp != "": final_df = data1[data1['Pincode'] == pincode_inp]

    age_inp = streamlit.sidebar.selectbox('Select Minimum Age', [""] + valid_age)
    if age_inp != "": final_df = data1[data1['Minimum Age Limit'] == age_inp]

    cap_inp = streamlit.sidebar.selectbox('Select Availablilty', [""] + ["Available"])
    if cap_inp != "": data1[data1['Available Capacity'] > 0]

    table = deepcopy(data1)
    table.reset_index(inplace=True, drop=True)
    streamlit.table(table)
else:
    streamlit.error("Unable to fetch data currently, please try after sometime")

streamlit.markdown("**_-Rakesh Kumar_**")
