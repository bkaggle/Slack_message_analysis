import streamlit as st
import os, sys
import json
import glob
import re
from gensim import corpora
import pandas as pd
import pickle
from matplotlib import pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from wordcloud import WordCloud


with open('notebooks/lda_model.pkl', 'rb') as f:
    lda_model = pickle.load(f)
df = pd.read_csv('slack_data.csv')
reactions_df = pd.read_csv('data/reactions.csv')
mentions_df = pd.read_csv('data/mentions.csv')

df['msg_content'] = df['msg_content'] .astype(str) 
# Casting to type str 
df['msg_content']  = df['msg_content'] .apply(lambda x: x.lower())
# Converting rows under the column 'full_text' to lowercase
df['msg_content']  = df['msg_content'] .apply(lambda x: x.translate(str.maketrans(' ', ' ',' ')))

sentence_list = [message for message in df['msg_content']]
word_list = [sent.split() for sent in sentence_list]

id2word  = corpora.Dictionary(word_list)
corpus= [id2word.doc2bow(message) for message in word_list]

# Display the DataFrame
st.title("10 Academy")
# Function to generate word cloud from LDA model
def generate_wordcloud_from_text(text_list):
    text = ' '.join(text_list)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud


# Display the top users
Top_10_users_by_replies = df.groupby('sender_name')['reply_users_count'].sum().reset_index(name='Top_10_users_by_replies').sort_values(by='Top_10_users_by_replies', ascending=False).head(10)
Top_10_users_by_messages = df.groupby('sender_name').size().reset_index(name='Top_10_users_by_messages').sort_values(by='Top_10_users_by_messages', ascending=False).head(10)
Top_10_users_by_reactions = df.groupby('sender_name').size().reset_index(name='Top_10_users_by_reactions').sort_values(by='Top_10_users_by_reactions', ascending=False).head(10)
Top_10_users_by_mentions = mentions_df.groupby(['sender_name']).size().reset_index(name='Top_10_users_by_mentions').sort_values(by='Top_10_users_by_mentions', ascending=False).head(10)

st.header('Word Cloud from Streamlit')
wordcloud_text = ' '.join(df['msg_content'].tolist())
wordcloud = generate_wordcloud_from_text([wordcloud_text])
st.image(wordcloud.to_array(), width=800)

# Top Users Section
st.header('Top 10 Users by Replies')
st.table(Top_10_users_by_replies)

st.header('Top 10 Users by Messages')
st.table(Top_10_users_by_messages)

st.header('Top 10 Users by Reactions')
st.table(Top_10_users_by_reactions)

st.header('Top 10 Users by Mentions')
st.table(Top_10_users_by_mentions)

# Optional: Display the LDA model topics
st.header('LDA Model Topics')
for topic_num, words in lda_model.print_topics():
    st.write(f'Topic {topic_num}: {words}')