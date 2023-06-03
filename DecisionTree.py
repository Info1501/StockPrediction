import pandas_datareader.data as web
import datetime
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import tree
import graphviz

class DecisionTree:

    def BuildTreeModel(self):

        df = web.DataReader('AAPL', data_source='stooq', start='2012-01-01', end=datetime.date.today())

        df["Return"] = df["Open"].pct_change(85).shift(-85)
        list_of_features = ["High", "Low", "Close", "Volume", "Open"]
        X = df[list_of_features]
        Y = np.where(df.Return > 0.05, "Strong Buy",
                     np.where(df.Return < -0.05, "Strong Sell", np.where(df.Return > 0, "Buy", "Sell")))

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, stratify=Y)
        Tree = DecisionTreeClassifier(max_depth=4)
        Tree.fit(X_train, Y_train)
        Y_pred = Tree.predict(X_test)
        report = classification_report(Y_test, Y_pred)
        st.text(report)
        data = tree.export_graphviz(Tree, filled=True, feature_names=list_of_features,class_names=["Strong Buy", "Strong Sell", "Buy", "Sell"])
        st.write("## AAPL Stock Decision Tree")
        st.graphviz_chart(data)
    def BuildTreeReal(self,stock):


        try:
            end = datetime.date.today()
            start = end - datetime.timedelta(days=1800)
            df = web.DataReader(stock, data_source='stooq', start=start, end=end)
            list_of_features = ["High", "Low", "Close", "Volume", "Open"]
            df["Return"] = df["Open"].pct_change(5).shift(-5)
            df["Signal"] = np.where(df["Return"] > 0.05, "Strong Buy", np.where(df["Return"] < -0.05, "Strong Sell",np.where(df["Return"] > 0, "Buy", "Sell")))
            X = df[list_of_features]
            Y = df["Signal"]

            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, stratify=Y)

            Tree = DecisionTreeClassifier(max_depth=4)
            Tree.fit(X_train, Y_train)

            st.write(
                "This is the accuracy report of the tree based on a 5 years worth of data on your desired stock or since it appeared on the exchange")
            Y_pred = Tree.predict(X_test)
            report = classification_report(Y_test, Y_pred)
            st.text(report)

            st.write("This is the decision provided by the algorithm based on the data until today. You can see its precision on the test set in the report above.")
            X_current = X.tail(1)
            Y_pred_final = Tree.predict(X_current)

            decision = Y_pred_final[0]

            if decision == "Strong Sell":
                st.image("assets/sstrong.png")
            elif decision == "Strong Buy":
                st.image("assets/strong.png")
            elif decision == "Sell":
                st.image("assets/Sell.png")
            elif decision == "Buy":
                st.image("assets/Buy.png")
        except Exception as e:
            print(e)
            st.write("### There is no such stock ticker !!")







