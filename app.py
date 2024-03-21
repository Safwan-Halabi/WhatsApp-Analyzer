import streamlit as st
import re
import matplotlib.pyplot as plt
import numpy as np
import preprocess
import stats
import pandas as pd

st.sidebar.title("WhatsApp Chat Analyzer")

# Uploading a file

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    # Converting bytecode to text-file

    data = bytes_data.decode('utf-8')

    df = preprocess.preprocess(data)

    # Unique users
    user_list = df['User'].unique().tolist()

    # Remove group notifications from user_list
    user_list.remove('Group Notification')

    # Sort for good measure
    user_list.sort()

    # Insert the word "Overall" at the start of the list
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox(
        'Show analysis with respect to',user_list)
    
    st.title('WhatsApp chat analysis for ' + selected_user)
    if st.sidebar.button("Show Analysis"):
        

        # TESTING
        st.dataframe(df['Message'])


        # Fetch user data
        num_messages, num_words, media_omitted, links = stats.fetchstats(
            selected_user, df)
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total No. of Words")
            st.title(num_words)

        with col3:
            st.header("Media Omitted")
            st.title(media_omitted)

        with col4:
            st.header("Total Links Shared")
            st.title(links)
        
        # Finding the busiest users in the group
        
        if selected_user == 'Overall':

            # Here were gonna need 2 columns, 1 for a chart and 1 for a dataframe
            st.title("Most Busy Users")
            busycount, newdf = stats.fetchbusyuser(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(busycount.index, busycount.values, color='Red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(newdf)
            

        # Creating the WordCloud
        
        st.title("Word Cloud")
        df_img = stats.createwordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)

        # Most Common Words in the Chat

        most_common_df = stats.getcommonwords(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)
        
        # Emoji Analysis

        emoji_df = stats.getemojistats(selected_user, df)

        st.title("Emoji Analysis")
        
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            emojicount = list(emoji_df['Count'])
            perlist = [(i/sum(emojicount))*100 for i in emojicount]
            emoji_df['Percentage use'] = np.array(perlist)
            st.dataframe(emoji_df)

        # Monthly Timeline
        
        st.title('Monthly Timeline')
        time = stats.monthtimeline(selected_user, df)
        fig, ax = plt.subplots()
        dates = [date for date in time['Time']]
        ax.plot(np.arange(1,len(time['Message'])+1), time['Message'], color='green')
        ax.set_xticks(np.arange(1,len(time['Message'])+1))
        ax.set_xticklabels(dates)        
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)
        
        
        # Activity maps

        st.title("Activity Maps")
        
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = stats.weekactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)
            

