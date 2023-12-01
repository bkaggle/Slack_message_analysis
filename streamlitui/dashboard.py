import streamlit as stl
import os, sys
import json
import glob
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from wordcloud import WordCloud


def convert_2_timestamp(column, data):
    """convert from unix time to readable timestamp
        args: column: columns that need to be converted to timestamp
                data: data that has the specified column
    """
    if column in data.columns.values:
        data[column] = pd.to_datetime(data[column], unit='s', errors='coerce')
        return data[column]
    else:
        print(f"{column} not in data")

message_with_user = pd.read_csv('week8.csv')
stl.set_option('deprecation.showPyplotGlobalUse', False)

msg_sent_standard_time = convert_2_timestamp("msg_sent_time", message_with_user)
message_with_user["msg_sent_standard_time"] = pd.to_datetime(msg_sent_standard_time)

### Parsing Data
slack_parser_df = pd.read_csv('slack_data.csv')

df = slack_parser_df.sort_values(by='msg_sent_time', ascending=True)
df['time_sent'] = convert_2_timestamp('msg_sent_time', df)
df['time_difference_seconds'] = df['time_sent'].diff().dt.total_seconds()

combined_df  = pd.DataFrame()

def draw_avg_reply_count(data, channel='Random'):
    """who commands many replies?"""

    fig, ax = plt.subplots(figsize=(15, 7.5))
    data.groupby('sender_name')['reply_count'].mean().sort_values(ascending=False)[:20]\
        .plot(kind='bar', ax=ax)
    
    ax.set_title(f'Average Number of reply count per Sender in #{channel}', size=20, fontweight='bold')
    ax.set_xlabel("Sender Name", size=18)
    ax.set_ylabel("Frequency", size=18)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)

    # Return the Matplotlib figure
    return fig


stl.set_page_config(page_title="10 Academy week0", page_icon=":ninja:", layout="wide")
# Header section

# Body Section
with stl.container():
    stl.subheader("Hi, I am mike :wave:")
    stl.title("This is a presentation of my finding for task 1 and 2")
with stl.container():
    stl.write("---")
    left_column, right_column = stl.columns([0.3, 0.7])
    with left_column:
        stl.header("Task 1")
        stl.write("##")
        stl.write("""
        Average number of reply count per Sender in the channel random
        """)
    with right_column:
        stl.pyplot(draw_avg_reply_count(slack_parser_df))
with stl.container():
    stl.write("---")
    left_column, right_column = stl.columns([0.3, 0.7])
    with left_column:
        stl.header("Task 2")
        stl.write("##")
        stl.write("""
        Histogram of the time difference between Consecutive messages
        """)
    with right_column:
        df['time_difference_seconds'] = df.groupby("msg_type")["msg_sent_standard_time"].diff()

        # Plot the histogram
        fig, ax = plt.subplots()
        ax.hist( df[df["msg_type"] == 'message']["time_difference"].dt.total_seconds() / 60,
                bins=10,
                edgecolor='black')
        ax.set_title('Time Differences between Consecutive Messages')
        ax.set_xlabel('Time Difference (minutes)')
        ax.set_ylabel('Frequency')
        # Display the plot using Streamlit
        stl.pyplot(fig)
with stl.container():
    stl.write("---")
    left_column, right_column = stl.columns([0.3, 0.7])
    with left_column:
        stl.header("Task 2")
        stl.write("##")
        stl.write("""
        Histogram of the time difference between Consecutive replys of a message
        """)
    with right_column:
        fig, ax = plt.subplots()
        ax.hist(combined_df['time_difference'].dt.total_seconds() / 60, bins=15, edgecolor='black')
        ax.set_title('Time Differences between Consecutive Replies (Combined Data)')
        ax.set_xlabel('Time Difference (minutes)')
        ax.set_ylabel('Frequency')

        # Display the plot using Streamlit
        stl.pyplot(fig)