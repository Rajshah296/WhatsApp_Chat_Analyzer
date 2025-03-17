import streamlit as st
import preprocessor, helper
import plotly.express as px
import plotly.graph_objects as go

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
    
    selected_user = st.sidebar.selectbox("Show analysis wrt: ", users)
    
    if st.sidebar.button("Show Analysis"):
        
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
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
        
        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig = px.line(timeline, x='time', y='message', title='Monthly Messages Trend', markers=True)
        st.plotly_chart(fig)
        
        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        
        with col1:
            st.header('Most busy days')
            busy_days = helper.week_activity_map(selected_user, df)
            fig = px.bar(x=busy_days.index, y=busy_days.values, title='Most Active Days', labels={'x': 'Day', 'y': 'Messages'})
            st.plotly_chart(fig)
            
        with col2:
            st.header('Most busy Months')
            busy_months = helper.month_activity_map(selected_user, df)
            fig = px.bar(x=busy_months.index, y=busy_months.values, title='Most Active Months', labels={'x': 'Month', 'y': 'Messages'})
            st.plotly_chart(fig)
        
        # Activity Heatmap
        st.title('Weekly Activity Heatmap')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig = px.imshow(user_heatmap, labels=dict(x='Hour', y='Day', color='Messages'), color_continuous_scale='magma')
        st.plotly_chart(fig)
        
        # Busiest Users (if overall selected)
        if selected_user == "Overall":
            st.title("Most Busy Users")
            user_counts, new_df = helper.fetch_most_busy_users(df)
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(x=user_counts.index, y=user_counts.values, title='Most Active Users', labels={'x': 'User', 'y': 'Messages'})
                st.plotly_chart(fig)
                
            with col2:
                st.dataframe(new_df)
        
        # WordCloud
        df_wc = helper.get_wordcloud(selected_user, df)
        st.title('WordCloud')
        st.image(df_wc.to_array(), use_container_width=True)
        
        # Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)
        fig = px.bar(most_common_df, x='count', y='word', orientation='h', title='Most Common Words', labels={'count': 'Frequency', 'word': 'Word'})
        st.plotly_chart(fig)
        
        # Emoji Analysis
        emoji_df = helper.most_common_emoji(selected_user, df)
        st.title('Emoji Analysis')
        st.dataframe(emoji_df)
