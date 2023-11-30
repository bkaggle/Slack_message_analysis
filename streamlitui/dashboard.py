import streamlit as stl
import os, sys
import json
import glob
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from wordcloud import WordCloud



# Add parent directory to path to import modules from src
rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

from src.loader import SlackDataLoader
import src.utils as utils


### Parsing Data
data_directory = os.path.join(rpath, "data")
slack_data_loader = SlackDataLoader(data_directory)
# List all directories in the 'data' directory
directories = [d for d in os.listdir(data_directory) if os.path.isdir(os.path.join(data_directory, d))]


dfs_by_directory = []

# Iterate through each directory
for directory in directories:
    directory_path = os.path.join(data_directory, directory)
    df_directory = slack_data_loader.slack_parser(directory_path)
    
    # Add a 'directory' column to identify the source directory
    df_directory['directory'] = directory
    
    # Append the DataFrame to the list
    dfs_by_directory.append(df_directory)

# Concatenate all DataFrames into a single DataFrame
slack_parser_df = pd.concat(dfs_by_directory, ignore_index=True)

df = slack_parser_df.sort_values(by='msg_sent_time', ascending=True)
df['time_sent'] = utils.convert_2_timestamp('msg_sent_time', df)
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