import datetime
import pandas_datareader.data as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import taew as elliott
class Eliott:

    def Waves(self,stock):

        end = datetime.date.today()
        start = end - datetime.timedelta(days=30)
        df = web.DataReader(stock, data_source='stooq', start=start, end=end)

        prices = df.filter(["Close", "Open"])
        prices = prices[::-1]
        values = df.filter(["Close"])
        plt.figure(figsize=(16, 8))
        plt.title("Pattern")
        plt.xlabel("Date", fontsize=18)
        plt.ylabel("Closing", fontsize=18)

        plt.plot(values, label="Values")

        upward_waves = self.RecognizeUpward(prices)
        downward_waves = self.RecognizeDownward(prices)
        corrective_upward_moves = self.RecognizeCorrectiveUpward(prices)
        corrective_downward_moves = self.RecognizeCorrectiveDownward(prices)

        if not upward_waves.empty:
            plt.scatter(upward_waves.index, upward_waves["Close"], c='green', label='Upward Waves',s=90)

        if not downward_waves.empty:
            plt.scatter(downward_waves.index, downward_waves["Close"], c='red', label='Downward Waves',s=90)

        if not corrective_upward_moves.empty:
            plt.scatter(corrective_upward_moves.index, corrective_upward_moves["Close"], c='orange',
                        label='Corrective Upward Moves')

        if not corrective_downward_moves.empty:
            plt.scatter(corrective_downward_moves.index, corrective_downward_moves["Close"], c='black',
                        label='Corrective Downward Moves')

        plt.legend()
        st.pyplot(plt)

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
