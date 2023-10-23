import streamlit as st
import pandas as pd
import numpy as np

# st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Uber Pickups Demo", page_icon=":taxi:")

with st.sidebar:
   st.radio('Select one:', [1, 2])

st.header("Uber NYC Pickup point")

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

row2_col1, padding,row2_col2 = st.columns((10,2,10))

col1, padding,col2 = st.columns((10,2,10))

with row2_col1:
    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache_data)")

    # if st.checkbox('Show raw data'):
    #     st.subheader('Raw data')
    #     st.write(data)

with row2_col2:
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]


with col1:
    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
    bc = st.bar_chart(hist_values)


with col2:
    # Some number in the range 0-23
    st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    st.map(filtered_data)



if st.button('reset'):
    st.write('reset')

if st.button('Say hello'):
    st.write('Why hello there')