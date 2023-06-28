import yfinance as yf
import pandas as pd
import time
import streamlit as st
class Piotrosky:

    def Grade(self,stock):
        try:
            total_score = 0
            profitability_score = 0
            leverage_score = 0
            operating_efficiency = 0
            data = yf.Ticker(stock)
            balance_sheet = data.balance_sheet
            income_statement = data.income_stmt
            cfs = data.cashflow
            years = balance_sheet.columns
            #Score 1
            net_income = income_statement[years[0]]['Net Income']
            net_income_py = income_statement[years[1]]['Net Income']
            profitability_score = 1+profitability_score if net_income > net_income_py else profitability_score
            #Score 2
            op_cf = cfs[years[0]]['Cash Flow From Continuing Operating Activities']
            profitability_score = 1+profitability_score if op_cf > 0 else profitability_score
            #Score 3
            avg_assets = (balance_sheet[years[0]]['Total Assets']
                        + balance_sheet[years[1]]['Total Assets']) / 2
            avg_assets_py = (balance_sheet[years[1]]['Total Assets']
                            +  balance_sheet[years[2]]['Total Assets']) / 2
            RoA = net_income / avg_assets
            RoA_py = net_income_py / avg_assets_py
            profitability_score = 1+profitability_score if RoA > RoA_py else profitability_score
            #Score 4
            total_assets = balance_sheet[years[0]]['Total Assets']
            accruals = op_cf / total_assets - RoA
            profitability_score = 1+profitability_score if accruals > 0 else profitability_score
            #Score 5
            try:
                lt_debt = balance_sheet[years[0]]['Long Term Debt']
                total_assets = balance_sheet[years[0]]['Total Assets']
                debt_ratio = lt_debt / total_assets
                leverage_score = 1+leverage_score if debt_ratio < 0.4 else leverage_score
            except:
                leverage_score = 1+leverage_score
            #Score 6
            current_assets = balance_sheet[years[0]]['Current Assets']
            current_liab = balance_sheet[years[0]]['Current Liabilities']
            current_ratio = current_assets / current_liab
            leverage_score = 1+leverage_score if current_ratio > 1 else leverage_score
            #Score 7
            gp = income_statement[years[0]]['Gross Profit']
            gp_py = income_statement[years[1]]['Gross Profit']
            revenue = income_statement[years[0]]['Total Revenue']
            revenue_py = income_statement[years[1]]['Total Revenue']
            gm = gp / revenue
            gm_py = gp_py / revenue_py
            operating_efficiency = 1+operating_efficiency if gm > gm_py else operating_efficiency
            #Score 8
            avg_assets = (balance_sheet[years[0]]['Total Assets']
                        + balance_sheet[years[1]]['Total Assets']) / 2
            avg_assets_py = (balance_sheet[years[1]]['Total Assets']
                            + balance_sheet[years[2]]['Total Assets']) / 2

            at = revenue / avg_assets
            at_py = revenue_py / avg_assets_py
            operating_efficiency = 1+operating_efficiency if at > at_py else operating_efficiency

            total_score = operating_efficiency + leverage_score + profitability_score

            match profitability_score:
                case 4:
                    profitability = '<p style="font-family:sans-serif; color:Green; font-size: 20px;">Profitabilty of company : 3</p>'
                    st.markdown(profitability, unsafe_allow_html=True)
                case 3:
                    profitability = '<p style="font-family:sans-serif; color:Green; font-size: 20px;">Profitabilty of company : 3</p>'
                    st.markdown(profitability,unsafe_allow_html=True)
                case 2:
                    profitability = '<p style="font-family:sans-serif; color:Yellow; font-size: 20px;">Profitabilty of company : 2</p>'
                    st.markdown(profitability, unsafe_allow_html=True)
                case 1:
                    profitability = '<p style="font-family:sans-serif; color:Orange; font-size: 20px;">Profitabilty of company : 1</p>'
                    st.markdown(profitability, unsafe_allow_html=True)
                case 0:
                    profitability = '<p style="font-family:sans-serif; color:Red; font-size: 20px;">Profitabilty of company : 0</p>'
                    st.markdown(profitability, unsafe_allow_html=True)
            match leverage_score:
                    case 2:
                        leverage = '<p style="font-family:sans-serif; color:Green; font-size: 20px;">Leverage, Liquidity and Source of Funds rating: 2</p>'
                        st.markdown(leverage, unsafe_allow_html=True)
                    case 1:
                        leverage = '<p style="font-family:sans-serif; color:Orange; font-size: 20px;">Leverage, Liquidity and Source of Funds rating: 1</p>'
                        st.markdown(leverage, unsafe_allow_html=True)
                    case 0:
                        leverage = '<p style="font-family:sans-serif; color:Red; font-size: 20px;">Leverage, Liquidity and Source of Funds rating: 0</p>'
                        st.markdown(leverage, unsafe_allow_html=True)
            match operating_efficiency:
                    case 2:
                        efficiency = '<p style="font-family:sans-serif; color:Green; font-size: 20px;">Operating Efficiency of company: 2</p>'
                        st.markdown(efficiency, unsafe_allow_html=True)
                    case 1:
                        efficiency = '<p style="font-family:sans-serif; color:Orange; font-size: 20px;">Operating Efficiency of company: 1</p>'
                        st.markdown(efficiency, unsafe_allow_html=True)
                    case 0:
                        efficiency = '<p style="font-family:sans-serif; color:Red; font-size: 20px;">Operating Efficiency of company: 0</p>'
                        st.markdown(efficiency, unsafe_allow_html=True)
            match total_score:
                    case 8:
                        st.image("assets/strong.png")
                    case 7:
                        st.image("assets/Buy.png")
                    case 2:
                        st.image("assets/Sell.png")
                    case 1:
                        st.image("assets/sstrong.png")
                    case 0:
                        st.image("assets/sstrong.png")
                    case _:
                        st.image("assets/hold.png")
        except Exception:
            st.write("### There is no such stock ticker !!")





