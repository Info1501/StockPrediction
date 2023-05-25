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
        list_of_features=["High","Low","Close","Volume","Open"]
        X = df[list_of_features]
        Y = np.where(df.Return > 0 , "Buy" , "Sell")
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.3,stratify=Y)
        Tree = DecisionTreeClassifier(max_depth=3)
        Tree.fit(X_train,Y_train)
        Y_pred =Tree.predict(X_test)
        report = classification_report(Y_test,Y_pred)
        st.text(report)
        data = tree.export_graphviz(Tree,filled=Tree,feature_names=list_of_features,class_names=np.array(["Buy","Sell"]),)
        st.write("## AAPL Stock Decision Tree")
        st.graphviz_chart(data)

    def BuildTreeReal(self,stock):


        try:
            end = datetime.date.today()
            start = end - datetime.timedelta(days=1800)
            df = web.DataReader(stock, 'stooq', start, end)
            list_of_features = ["High", "Low", "Close", "Volume", "Open"]
            df["Return"] = df["Open"].pct_change(5).shift(-5)

            X = df[list_of_features]
            Y = np.where(df.Return > 0, "Buy", "Sell")
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, stratify=Y)
            Tree = DecisionTreeClassifier(max_depth=4)
            Tree.fit(X,Y)
            st.write("This is the accuracy report of the tree based on a 5 years worth of data on your desired stock or since it appeared on the exchange")
            Y_pred = Tree.predict(X_test)
            report = classification_report(Y_test, Y_pred)
            st.text(report)
            st.write("This is the decision provided by the alogrithm based on the data until today . You can see it's precision on the set test in the report above. ")
            Y_pred_final = Tree.predict(X.tail(1))
            if "Sell"== Y_pred_final[0]:
                st.image("Sell.png")
            if "Buy" == Y_pred_final[0]:
                st.image("Buy.png")
        except:
            st.write("### There is no such stock ticker !!")







