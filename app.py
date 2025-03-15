import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader('Choose a File: ')
if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    
    users = df['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0,'Overall')
    
    selected_user = st.sidebar.selectbox("Show analysis wrt: ",users)
    
    if st.sidebar.button("Show Analysis"):
        
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
            
            
        # monthly timeline
        
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Activity Map
        
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        
        with col1:
            st.header('Most busy days')
            busy_days = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_days.index, busy_days.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.header('Most busy Months')
            busy_months = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_months.index, busy_months.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        # Activity Heatmap
        st.title('Weekly Activity Heatmap')
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap,cmap='magma')
        st.pyplot(fig)
        
        # Who is/are the busiest users in the chat?
    
        if(selected_user == "Overall"):
            st.title("Most Busy users")
            user_counts,new_df   = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(user_counts.index,user_counts.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_df)
                
        # WordCloud
        
        df_wc = helper.get_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.title('WordCloud')
        st.pyplot(fig)
        
        # most common words 
        
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df['word'],most_common_df['count'])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig) 
        
        # most common emojis
        
        emoji_df = helper.most_common_emoji(selected_user,df)
        st.title('Emoji Analysis')
        st.dataframe(emoji_df)
        

        