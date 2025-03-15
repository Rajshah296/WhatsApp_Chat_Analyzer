import pandas as pd
import re


def preprocess(data):

    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*\u202F?[ap]m\s-\s"

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)
    dates = [i.replace("\u202F", " ") for i in dates]

    df = pd.DataFrame({'user_message': messages, 'date':dates})
    #convert message_date type

    df['date'] = pd.to_datetime(df['date'],format = '%d/%m/%y, %I:%M %p - ')


    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df = df.drop(columns=['user_message'],axis=1)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['AM/PM'] = df['date'].dt.strftime('%p')
    df['24_hour_format'] = df.apply(lambda row: row['hour'] if row['AM/PM'] == 'AM' else (row['hour'] if row['hour'] == 12 else row['hour'] + 12), axis=1)
    
    df['period'] = df['24_hour_format'].apply(lambda x : f'{x}-00' if x+1 == 24 else f'{x}-{x+1}')
    
    df = df.drop(['date'],axis=1)

    return df