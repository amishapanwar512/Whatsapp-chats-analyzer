from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]
    #fetch number of messages
    num_messages = df.shape[0]

    #fetch number of words
    words=[]
    for message in df['messages']:
        words.extend(message.split())
        #fetch number of media items
        num_media_msg=df[df['messages'] == '<Media omitted>\n']

        return num_messages,len(words), len(num_media_msg)
def most_busy_user(df):
    x=df['user'].value_counts().head()
    df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x,df

def create_wordscloud(selected_user,df):
    f=open('stop_words.txt','r')
    stop_words=f.read()
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notifications']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc=WordCloud(width=500, height=500, min_font_size=10,background_color='white')
    temp['messages']=temp['messages'].apply(remove_stop_words)
    df_wc=wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop_words.txt','r')
    stop_words=f.read()

    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]
    temp=df[df['user']!='group_notifications']
    temp=temp[temp['messages']!='<Media omitted>\n']
    words=[]
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df=pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])
    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']=time

    return   timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = (df.groupby('onlyDate').count()['messages'].reset_index())[1:254]
    return daily_timeline

def busiest_day(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Return the value counts of messages per day
    return df['day_name'].value_counts()
def busiest_month(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Return the value counts of messages per day
    return df['month'].value_counts()
