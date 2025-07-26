import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

st.title("chd del")

# --- Inputs ---
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
days = st.number_input("How many days do you want to calculate?", min_value=1, max_value=100, value=10)
date = st.text_input("Enter the start date (DD-MMM-YYYY)", value="17-JUN-2024")
show_graph = st.checkbox("Do you want a graph?")

if uploaded_file and st.button("Run Analysis"):
    try:
        closing = pd.read_csv(uploaded_file)
        closing.index = range(len(closing))
        closing.index = closing.index.astype(int)

        if closing['close '].dtype == object:
            closing['close '] = closing['close '].str.replace(',', '', regex=True)

        closing['close '] = closing['close '].astype(float)

        ind = (closing[closing['Date '] == date].index)
        if len(ind) == 0:
            st.error("Date not found in CSV.")
        else:
            intind = int(ind[0])
            chd = []

            for _ in range(days):
                profit = []
                loss = []

                for i in range(intind, intind + 14):
                    diff = closing.iloc[i+1]['close '] - closing.iloc[i]['close ']
                    if diff < 0:
                        loss.append(-diff)
                    else:
                        profit.append(diff)

                total_gain = sum(profit)
                total_loss = sum(loss)
                c = 100 - (total_gain / (total_gain + total_loss)) * 100 if (total_gain + total_loss) != 0 else 0
                chd.append(float(c))
                intind += 1

            st.subheader("CHD Values")
            st.write(chd[::-1])

            if show_graph:
                st.subheader("Graph")
                xpoints = np.array(range(1, days + 1))
                ypoints = np.array(chd[::-1])

                fig, ax = plt.subplots()
                ax.plot(xpoints, ypoints, marker='o')
                ax.axhline(30, color='red', linestyle='--', label='Threshold = 30')
                ax.set_xlabel("Day")
                ax.set_ylabel("CHD Value")
                ax.legend()
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")
 #dont forget to type "streamlit run chdupdated.py" in the terminal below