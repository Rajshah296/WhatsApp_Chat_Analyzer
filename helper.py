from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import wordcloud 
from collections import Counter
import pandas as pd
import emoji

extractor = URLExtract()

def fetch_stats(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    # fetch the number of messages
    num_messages = df.shape[0]
    # fetch the number of words    
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)
    
    # fetch the number of media shared.
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    links = []

    for message in df['message']:
        urls = extractor.find_urls(message)
        links.extend(urls)
    num_links = len(links)
        
    return num_messages,num_words, num_media,num_links

def fetch_most_busy_users(df):
    
    user_counts = df['user'].value_counts().sort_values(ascending=False)
    new_df = round((df['user'].value_counts().sort_values(ascending=False)/df.shape[0]) * 100,2).reset_index().rename(columns = {'index':'user','user':'percent'})
    return user_counts.head(),new_df

def get_wordcloud(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    f = open('stop_hinglish.txt','r')
    stopwords = f.read()
    
    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['user'] != 'group_notification']
    
    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
                
        return " ".join(words)
        
    wc = wordcloud.WordCloud(width=500,height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    
    f = open('stop_hinglish.txt','r')
    stopwords = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['user'] != 'group_notification']
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
                
    return_df = pd.DataFrame(Counter(words).most_common(20), columns=['word','count'])
    return  return_df

def most_common_emoji(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
        
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        
    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emoji','Count'])

def monthly_timeline(selected_user, df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
        
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def week_activity_map(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
        
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
        
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap