from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud

import emoji

extract = URLExtract()

def fetchstats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Counting messages and words
    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())
    
    # Counting media files shared
    mediaomitted = df[(df['Message'] == '<Media omitted>') | (df['Message'] == ' <media omitted>')]

    # Counting links shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words), mediaomitted.shape[0], len(links)


def fetchbusyuser(df):
    df = df[df['User'] != "Group Notification"]
    count = df['User'].value_counts().head()

    newdf = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count, newdf


def createwordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))
    
    return df_wc

def getcommonwords(selected_user, df):

    # We need to filter out the stopwords!
    file = open('stop_hinglish.txt','r')
    stopwords = file.read()
    stopwords = stopwords.split('\n')

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    temp = df[(df['User'] != 'Group Notification') | (df['User'] != '<Media omitted>') | (df['User'] != '<media omitted>')]

    words = []

    for message in df['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
        
    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon


def getemojistats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message']:
        for em in emoji.emoji_list(message):
            emojis.append(em['emoji'])
        #emojis.extend([c for c in message if emoji.emoji_list(c)])
    
    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns =['Emoji','Count'])
    return emojidf


def monthtimeline(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    temp = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()
    
    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i] + "-" + str(temp['Year'][i]))
    
    temp['Time'] = time
    return temp


def weekactivitymap(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    return df['Day_name'].value_counts()

