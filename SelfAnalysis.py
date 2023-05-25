import streamlit as st
import datetime
import math
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt

class Self:


    def Graph(self,stock,start_date,end_date):

        try:
            df = web.DataReader(stock, data_source='stooq',start = start_date,end= end_date)
            df["Open"]
            st.write("## Closing Price")
            st.line_chart(df.filter(['Close']))
            st.write("## Volume")
            st.line_chart(df.filter(['Volume']))
            st.write(df)
        except:
            st.write("### There is no such stock ticker !!")


