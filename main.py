# This is a sample Python script.
import datetime

import LSTM
import streamlit as st
import SelfAnalysis as sa
import DecisionTree as dt
import EliottWaves as ew
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.write("# Intelligent Systems based on Stock Market Analysis")

    lstm = LSTM.LSTModel()
    option = st.selectbox('What type of analysis would you like to use ?',("Self Analsysis","LSTM","Decision Tree","Elliot Waves"))
    if option == "LSTM":

        new_option = st.selectbox('Would you like to learn more about LSTM or see the real thing?',("Select Here","Learn More","LSTM Price Prediction"))
        if new_option == "Learn More":
            st.write("## What is LSTM and how does it work ?")
            st.write('''LSTM (Long Short-Term Memory) is a type of recurrent neural network (RNN) that is well-suited for processing and making predictions based on time series data, such as stock prices. LSTM networks are capable of learning long-term dependencies in the input data and can be used to predict future values of a time series based on its past values.

Here's a brief overview of how LSTM stock prediction works:''')

            st.markdown("Input data: The LSTM algorithm starts by analyzing historical stock price data, such as opening and closing prices, volume, and technical indicators.")
            st.markdown("Preprocessing: The input data is preprocessed to normalize the values and make them suitable for use in the LSTM network.")
            st.markdown("Time series input: The preprocessed data is fed into the LSTM network as a time series. Each time step represents a single observation in the time series, such as a daily closing price.")
            st.markdown("Training: The LSTM network is trained using the historical data to learn the patterns and relationships in the time series data.")
            st.markdown("Prediction: Once the LSTM network is trained, it can be used to make predictions about future values of the time series. The network takes the most recent values of the time series as input and generates a prediction for the next time step.")
            st.markdown("Iteration: The process of prediction and input continues iteratively, allowing the LSTM network to generate a sequence of predicted values for the time series.")
            lstm.BuildModel_Test()
        if new_option == "LSTM Price Prediction":
            stock = st.text_input(label='Stock Ticker',value="AAPL")
            lstm.BuildModel_Real(stock)
    if option == "Self Analsysis":

        col1, col2= st.columns([1, 1])

        with col1:
            start_date = st.date_input(label="Start Date", value=datetime.date.today() - datetime.timedelta(days=360))
        with col2:
            end_date = st.date_input(label="End Date", value=datetime.date.today())

        self = sa.Self()
        stock = st.text_input(label='Stock Ticker', value="AAPL")
        self.Graph(stock,start_date,end_date)

    if option == "Decision Tree":
        new_option = st.selectbox('Would you like to learn more about Decision Tree or see the real thing?',
                                  ("Select Here", "Learn More", "Decision Tree Trend Prediction"))

        if new_option == "Learn More":
            st.write("## What is a Decision Tree algorithm and how does it work?")
            st.write("Decision trees are a type of machine learning algorithm that can be used to identify the most important variables that influence market movements. They can be used to generate trading signals based on these variables. Here's a brief overview of how decision tree stock prediction works:")
            st.markdown("Input data: The decision tree algorithm starts by analyzing historical market data, such as prices, trading volume, and technical indicators.")
            st.markdown("Splitting criteria: The algorithm then identifies the most important variables that are likely to impact future market movements. These variables are used as splitting criteria for the decision tree.")
            st.markdown("Nodes: The decision tree consists of nodes that represent different possible outcomes based on the splitting criteria. Each node has one or more branches, representing different possible values of the splitting criteria.")
            st.markdown("Leaves: The final nodes of the decision tree are called leaves, and they represent the predicted outcomes of the decision tree. In the case of stock prediction, the leaves typically generate trading signals based on the variables identified by the splitting criteria.")
            st.write("The decision tree algorithm generates a tree-like model that captures the relationship between the input variables and the output variable, which is the stock price or a binary signal (buy or sell). The model is trained using historical market data, which allows it to learn which variables are the most important for predicting future market movements. The decision tree can then be used to make predictions about future market movements based on the variables identified by the splitting criteria.")
            st.write("In the report below we can observe multiple metric's that are used to evaluate a  Decision Tree :")
            st.markdown("Precision: This measures the proportion of positive predictions that were actually correct. It is calculated as the number of true positive predictions divided by the total number of positive predictions.")
            st.markdown("Recall: This measures the proportion of actual positives that were correctly identified. It is calculated as the number of true positive predictions divided by the total number of actual positives.")
            st.markdown("F1 Score: This is a weighted average of precision and recall, and provides a single value that summarizes the overall performance of the model.")
            st.markdown("Support: Refers to the number of instances or samples that belong to a particular node or leaf in the decision tree. In other words, it represents the number of data points that were used to generate a particular decision or prediction.")


            tree=dt.DecisionTree()
            tree.BuildTreeModel()


            st.write('''In the Decision Tree we can obseve the GINI index or Impurity.Gini index or Gini impurity is a measure of the impurity or randomness of a set of data points. It is commonly used in decision trees to evaluate the quality of a split or partition of data points based on a particular feature or attribute.

The Gini index ranges from 0 to 1, with 0 indicating a perfectly pure partition (i.e., all data points in the partition belong to the same class or category), and 1 indicating a perfectly impure partition (i.e., the data points in the partition are distributed evenly across all classes or categories).

To calculate the Gini index of a particular split in a decision tree, the following formula is used:

Gini index = 1 - Σ(p_i)^2

where p_i is the proportion of data points in the i-th class or category in the split.

The Gini index is used in the decision tree algorithm to determine the best split or partition of data points at each node, based on the attribute that maximizes the decrease in Gini impurity between the parent node and the child nodes. The split with the largest decrease in Gini impurity is chosen as the best split.''',)

        if new_option == "Decision Tree Trend Prediction":
            tree = dt.DecisionTree()
            stock = st.text_input(label='Stock Ticker', value="AAPL")
            tree.BuildTreeReal(stock)


    if option == "Elliot Waves":
        elliot = ew.Eliott()
        stock = st.text_input(label='Stock Ticker', value="AAPL")
        elliot.Waves(stock)
        st.write('''Elliott Wave Theory is a technical analysis approach that seeks to identify recurring patterns in financial markets. It is based on the idea that market prices move in waves, both in upward and downward directions, due to the psychology of market participants.

According to Elliott Wave Theory, price movements can be categorized into two types of waves: impulse waves and corrective waves. Impulse waves represent the main direction of the market trend, while corrective waves are counter-trend movements that occur within the larger trend.

The Elliott Wave principle suggests that price waves follow a specific pattern of five waves in the direction of the trend (impulse waves), followed by three waves in the opposite direction (corrective waves).''')
        st.markdown("Impulse waves:")
        st.markdown("- Wave 1: The initial wave in the direction of the trend.")
        st.markdown("- Wave 2: A corrective wave that retraces a portion of Wave 1.")
        st.markdown("- Wave 3: The strongest and longest wave that extends beyond Wave 1.")
        st.markdown("- Wave 4: Another corrective wave that retraces a portion of Wave 3.")
        st.markdown("- Wave 5: The final wave in the direction of the trend.")
        st.markdown("Corrective waves:")
        st.markdown("- Wave A: A corrective wave in the opposite direction of the trend.")
        st.markdown("- Wave B: A corrective wave that retraces a portion of Wave A.")
        st.markdown("- Wave C: The final corrective wave that moves in the opposite direction of the trend.")
        st.write("The Elliott Wave algorithm analyzes the price data of a stock and identifies potential upward and downward waves, as well as corrective upward and downward moves. It then visualizes these patterns on a graph.")
        st.write("While this code can help in identifying potential wave patterns in historical price data, it's important to note that Elliott Wave Theory is subjective and open to interpretation. ")



