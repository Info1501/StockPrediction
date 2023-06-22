import talib as ta
import pandas_datareader as web
import datetime
import streamlit as st
from Patterns import candlestick_patterns
import plotly.graph_objects as go
import pandas as pd
class CandleStick:

    def SearchPattern(self,pattern,stock):
        try:
            end = datetime.date.today()
            start = end - datetime.timedelta(days=30)
            df = web.DataReader(stock, data_source='stooq', start=start, end=end)

            for key in candlestick_patterns.keys():
                if candlestick_patterns.get(key) == pattern:
                    pattern_func = getattr(ta, key)
            result = pattern_func(df["Open"],df["High"],df["Low"],df["Close"])







            fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'])])
            fig.update_layout(
                title=f"{stock}'s adjusted stock price",
                yaxis_title="Price ($)"
            )
            found_pattern = dict()
            for date in result.index:
                if result[date] > 0:
                    fig.add_vline(x=date,line_width=3, line_dash="dash", line_color="green")

                if result[date] < 0:
                    fig.add_vline(x=date, line_width=3, line_dash="dash", line_color="red")

            st.plotly_chart(fig)
        except Exception as e:
            st.write("### There is no such stock ticker !!")