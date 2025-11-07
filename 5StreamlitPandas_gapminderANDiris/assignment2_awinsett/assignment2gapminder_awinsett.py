import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

st.markdown('# Gapminder Dashboard')

df = pd.read_csv('gapminder_data_graphs.csv')

unique_years = df['year'].unique()

selected_year = st.selectbox(label='Year', options=unique_years)

df_plot = df[df['year']==selected_year]

average_gdp = round(df_plot['gdp'].mean(),2)
average_life_exp = round(df_plot['life_exp'].mean(),2)
average_hdi = round(df_plot['hdi_index'].mean(),2)

col1, col2, col3 = st.columns([1,1,1])
col1.metric(label='Average GDP', value=average_gdp)
col2.metric(label='Average Life Expectancy', value=average_life_exp)
col3.metric(label='Average HDI', value=average_hdi)

title = 'Plot of GDP vs Life Expectency for Year {}'.format(selected_year)
scatter_plot = px.scatter(data_frame=df_plot, x='gdp', y='life_exp', color='continent', title=title)

st.plotly_chart(scatter_plot)

col4, col5 = st.columns(2)

boxplot1 = px.box(data_frame=df_plot, x='continent', y='gdp', title='Distribution fo GDP across the different continents for year {}'.format(selected_year))

histo_gdp = px.histogram(data_frame=df_plot, x='gdp', title='Distribution of GDP across the different continents for year{}'.format(selected_year))

col4.plotly_chart(boxplot1)
col5.plotly_chart(histo_gdp)

boxplot2 = px.box(data_frame=df_plot, x='continent', y='life_exp', title='Distribution fo Life Expectancy across the different continents for year{}'.format(selected_year))

histo_life = px.histogram(data_frame=df_plot, x='life_exp', title='Distribution of Life Expectancy across the different continents for year{}'.format(selected_year))

col4.plotly_chart(boxplot2)
col5.plotly_chart(histo_life)

boxplot3 = px.box(data_frame=df_plot, x='continent', y='hdi_index', title='Distribution fo HDI across the different continents for year{}'.format(selected_year))

histo_hdi = px.histogram(data_frame=df_plot, x='hdi_index', title='Distribution of HDI across the different continents for year{}'.format(selected_year))

col4.plotly_chart(boxplot3)
col5.plotly_chart(histo_hdi)