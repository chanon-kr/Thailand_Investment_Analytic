import streamlit as st
from datetime import datetime
import plotly.express as px
from function import get_invest_data, filter_df, format_df

@st.cache
def convert_df(df):
    return df.to_csv(index = False).encode('utf-8')

st.set_page_config(
     page_title="Investment Data Visualization",
     layout="wide",
     initial_sidebar_state="expanded",
 )

st.title('Investment Data Visualization')

col1, col2 = st.columns(2)

with col1:
    stock_type = st.selectbox('Select Type of Investment'
    ,('Common Stock'
    ,'Mutual fund'
    # , 'Common Stock'
    ))
    target_name = st.text_input('Name of Target Investment', 'SCC')

with col2:
    start_date = st.date_input("From",datetime(2022,1,1))
    end_date = st.date_input("To",datetime(2022,1,31))

if st.button('Show Data') :
    df = get_invest_data(stock_type, target_name, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    csv = convert_df(df)
    # col1, col2, col3 = st.columns(3) 
    # with col1:
    #     print( df['year'].unique())
    #     filter_year = st.multiselect('Filter Year', df['year'].unique())
    # with col2:
    #     filter_month = st.multiselect('Filter Month', df['month'].unique())
    # with col3:
    #     filter_month_year = st.multiselect('Filter Year-Month', df['year-month'].unique())
    # df_plot = filter_df(df, filter_year, filter_month, filter_month_year)
    st.title('All Data')
    x_ = 'Date'
    fig = px.line(df.sort_values(x_), x = x_, y = 'close_value')
    st.plotly_chart(fig, use_container_width=True)
    st.title('Group by Day')
    x_ = 'day'
    fig = px.box(df.sort_values(x_), x = x_, y="close_value", points="all")
    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2) 
    with col1 : 
        st.title('Group by Month')
        x_ = 'month'
        fig = px.box(df.sort_values(x_), x = x_, y="close_value", points="all")
        st.plotly_chart(fig, use_container_width=True)
        st.title('Group by Week Day')
        x_ = 'week_day'
        fig = px.box(df.sort_values(x_), x = x_, y="close_value", points="all")
        st.plotly_chart(fig, use_container_width=True)
        st.title('Raw Data')
        st.dataframe(df)
    with col2 : 
        st.title('Group by Year')
        x_ = 'year'
        fig = px.box(df.sort_values(x_), x = x_, y="close_value", points="all")
        st.plotly_chart(fig, use_container_width=True)
        st.title('Group by Month Period')
        x_ = 'month_period'
        fig = px.box(df.sort_values(x_), x = x_, y="close_value", points="all")
        st.plotly_chart(fig, use_container_width=True)
        st.title('Click to Download Data')
        st.download_button(
        "Download CSV",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
        )