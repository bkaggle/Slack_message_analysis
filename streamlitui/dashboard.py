import streamlit as st
import os, sys
import json
import glob
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from wordcloud import WordCloud


df = pd.read_csv('slack_data.csv')
# Display the DataFrame
st.title("10 Academy")
st.dataframe(df)

# Sidebar for filtering options
st.sidebar.title("Filter Options")

# Filtering by channel
selected_channel = st.sidebar.selectbox("Select Channel", df['channel'].unique())

# Filtering by message type
selected_msg_type = st.sidebar.selectbox("Select Message Type", df['msg_type'].unique())

# Filter the DataFrame based on user selection
filtered_df = df[(df['channel'] == selected_channel) & (df['msg_type'] == selected_msg_type)]

# Display filtered DataFrame
st.subheader("Filtered DataFrame")
st.dataframe(filtered_df)

# Visualize top 10 users by number of messages
st.subheader("Top 10 Users by Number of Messages")
top_messages_per_user = filtered_df['sender_name'].value_counts().nlargest(10)
st.bar_chart(top_messages_per_user)

# Visualize top 10 users by number of replies
st.subheader("Top 10 Users by Number of Replies")
top_replies_per_user = filtered_df.groupby('sender_name').size().nlargest(10)
st.bar_chart(top_replies_per_user)

# Visualize top 10 users by number of reactions
st.subheader("Top 10 Users by Number of Reactions")
top_reactions_per_user = filtered_df.groupby('sender_name')['reply_users_count'].size().nlargest(10)
st.bar_chart(top_reactions_per_user)