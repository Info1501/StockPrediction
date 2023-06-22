import datetime
import pandas_datareader.data as web
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
class Eliott:

    def Waves(self,stock):
        try:
            end = datetime.date.today()
            start = end - datetime.timedelta(days=30)
            df = web.DataReader(stock, data_source='stooq', start=start, end=end)

            prices = df.filter(["Close", "Open"])
            prices = prices[::-1]
            values = df.filter(["Close"])

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=values.index, y=values["Close"], name="Values"))

            upward_waves = self.RecognizeUpward(prices)
            downward_waves = self.RecognizeDownward(prices)
            corrective_upward_moves = self.RecognizeCorrectiveUpward(prices)
            corrective_downward_moves = self.RecognizeCorrectiveDownward(prices)

            if not upward_waves.empty:
                fig.add_trace(go.Scatter(
                    x=upward_waves.index,
                    y=upward_waves["Close"],
                    mode='markers',
                    name='Upward Waves',
                    marker=dict(color='green', size=15)
                ))

            if not downward_waves.empty:
                fig.add_trace(go.Scatter(
                    x=downward_waves.index,
                    y=downward_waves["Close"],
                    mode='markers',
                    name='Downward Waves',
                    marker=dict(color='red', size=15)
                ))

            if not corrective_upward_moves.empty:
                fig.add_trace(go.Scatter(
                    x=corrective_upward_moves.index,
                    y=corrective_upward_moves["Close"],
                    mode='markers',
                    name='Corrective Upward Moves',
                    marker=dict(color='orange', size=10)
                ))

            if not corrective_downward_moves.empty:
                fig.add_trace(go.Scatter(
                    x=corrective_downward_moves.index,
                    y=corrective_downward_moves["Close"],
                    mode='markers',
                    name='Corrective Downward Moves',
                    marker=dict(color='black', size=10)
                ))

            fig.update_layout(
                title="Pattern",
                xaxis_title="Date",
                yaxis_title="Closing",
                showlegend=True
            )

            st.plotly_chart(fig)
        except Exception as e:
            st.write("### There is no such stock ticker !!")

    def RecognizeUpward(self, prices):
        wave_patterns = pd.DataFrame(columns=["Close"])
        for i in range(len(prices) - 5):
            for j in range(i,i+4):
                start = j
                end = j
                wave = 1
                is_possible_wave = True
                while is_possible_wave and end < i+4:
                    if wave == 1:
                        if (
                            prices["Close"][start + 1] < prices["Close"][start]
                            and prices["Close"][start + 1] > prices["Open"][start]
                        ):
                            wave = 2
                            end += 1
                        else:
                            is_possible_wave = False
                    elif wave == 2 and end < i+4:
                        if prices["Close"][start + 1] < prices["Close"][start + 2]:
                            wave = 3
                            end += 1
                        else:
                            is_possible_wave = False
                    elif wave == 3 and end < i+4:
                        if (
                            prices["Close"][start + 2] > prices["Close"][start + 3]
                            and prices["Close"][start + 3] > prices["Close"][start]
                        ):
                            wave = 4
                            end += 1
                        else:
                            is_possible_wave = False
                    elif wave == 4 and end < i+4:
                        if prices["Close"][start + 3] < prices["Close"][start + 4]:
                            end += 1
                        else:
                            is_possible_wave = False

                if end == start:
                    is_possible_wave = False

                if is_possible_wave:
                    wave_patterns = wave_patterns.append(prices[start:end + 1])

        return wave_patterns

    def RecognizeDownward(self, prices):
        wave_patterns = pd.DataFrame(columns=["Close"])
        for i in range(len(prices) - 5):
            for j in range(i, i + 4):
                start = j
                end = j
                wave = 1
                is_possible_wave = True
                while is_possible_wave and end < i + 4:
                    if wave == 1:
                        if (
                                prices["Close"][start + 1] > prices["Close"][start]
                                and prices["Close"][start + 1] < prices["Open"][start]
                        ):
                            wave = 2
                            end += 1
                        else:
                            is_possible_wave = False
                    elif wave == 2 and end < i + 4:
                        if prices["Close"][start + 1] > prices["Close"][start + 2]:
                            wave = 3
                            end += 1
                        else:
                            is_possible_wave = False
                    elif wave == 3 and end < i + 4:
                        if (
                                prices["Close"][start + 2] < prices["Close"][start + 3]
                                and prices["Close"][start + 3] < prices["Close"][start]
                        ):
                            wave = 4
                            end += 1
                        else:
                            is_possible_wave = False
                    elif wave == 4 and end < i + 4:
                        if prices["Close"][start + 3] > prices["Close"][start + 4]:
                            end += 1
                        else:
                            is_possible_wave = False

                if end == start:
                    is_possible_wave = False

                if is_possible_wave:
                    wave_patterns = wave_patterns.append(prices[start:end + 1])

        return wave_patterns

    def RecognizeCorrectiveUpward(self, prices):
        corrective_moves = pd.DataFrame(columns=["Close"])
        for i in range(len(prices) - 3):
            start = i
            end = i + 3
            is_possible_move = True

            if (
                prices["Close"][start] < prices["Open"][start]
                and prices["Close"][start+1] > prices["Close"][start]
                and prices ["Close"][start+1] < prices["Open"][start]
                and prices ["Close"][start+1] > prices["Close"][start+2]
                ):
                corrective_moves = corrective_moves.append(prices[start:end])

        return corrective_moves

    def RecognizeCorrectiveDownward(self, prices):
        corrective_moves = pd.DataFrame(columns=["Close"])
        for i in range(len(prices) - 3):
            start = i
            end = i + 3
            is_possible_move = True

            if (
                    prices["Close"][start] > prices["Open"][start]
                    and prices["Close"][start + 1] < prices["Close"][start]
                    and prices["Close"][start + 1] > prices["Open"][start]
                    and prices["Close"][start + 1] < prices["Close"][start + 2]
            ):
                corrective_moves = corrective_moves.append(prices[start:end + 1])

        return corrective_moves
