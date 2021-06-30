import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Ontario COVID-19 Dashboard')
st.write('Created by Michal Jagodzinski')

data_url_general = 'https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv'
data_url_hospitals = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'

@st.cache
def load_data():
    data_general = pd.read_csv(data_url_general)
    data_hospitals = pd.read_csv(data_url_hospitals)

    return data_general, data_hospitals

data_general, data_hospitals = load_data()

ontario_filter = data_general['prname'] == 'Ontario'
ontario_data = data_general.loc[ontario_filter, :]

#st.write(ontario_data)
#st.write(data_hospitals)

st.markdown('# Daily Numbers')
day_data = ontario_data.tail(1)
day_data_hospital = data_hospitals.tail(1)

day_df = pd.DataFrame(data = {
    'New cases': [day_data['numtoday'].item()],
    'Deaths': [day_data['numdeathstoday'].item()],
    'Tests': [int(day_data['numteststoday'].item())],
    'In hospital': [day_data_hospital['Number of patients hospitalized with COVID-19'].item()],
    'In ICU': [day_data_hospital['Number of patients in ICU due to COVID-19'].item()],
    'In ICU on ventilator': [day_data_hospital['Number of patients in ICU on a ventilator due to COVID-19'].item()]
})

st.write(day_df)

st.markdown('# Cases Overview')

fig1 = px.line(
    ontario_data, 
    x="date", y="numtotal", 
    title='Total Confirmed Cases of COVID-19 in Ontario',
    labels = {
        "date": "Date",
        "numtotal": "Confirmed Cases"
    }
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    ontario_data, 
    x="date", y="numactive", 
    title='Active Cases of COVID-19 in Ontario',
    labels = {
        "date": "Date",
        "numactive": "Confirmed Cases"
    }
)
st.plotly_chart(fig2, use_container_width=True)

st.write('# Hospitalized Cases')

groups = [
    'Reported Date', 
    'Number of patients hospitalized with COVID-19', 
    'Number of patients in ICU due to COVID-19', 
    'Number of patients in ICU on a ventilator due to COVID-19'
]

data_hospitals_filtered = data_hospitals[groups]

data_hospitals_filtered = data_hospitals_filtered.dropna(thresh=2)
data_hospitals_filtered.columns = ['Date', 'In Hospital', 'In ICU', 'In ICU with Ventilator']

data_hospitals_filtered = pd.melt(data_hospitals_filtered, id_vars=['Date'], value_vars=['In Hospital', 'In ICU', 'In ICU with Ventilator'])
data_hospitals_filtered.columns = ['Date', 'Patient Type', 'Cases']

fig3 = px.line(
    data_hospitals_filtered, 
    x="Date", y="Cases", color = "Patient Type", 
    title='Hospitalized Cases of COVID-19 in Ontario'
)

st.plotly_chart(fig3, use_container_width=True)

st.write('# Variants Overview')