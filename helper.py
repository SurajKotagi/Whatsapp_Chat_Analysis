from urlextract import URLExtract
import re
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messeges
    number_of_messeges = df.shape[0]

    # fetch total number of words
    words = []
    for messeges in df['messege']:
        word_list = messeges.split()
        words.extend(word_list)
    word_count = len(words)

    # fetch number of media messges
    number_of_media_messeges = df[df['messege']
                                  == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for messege in df['messege']:
        links.extend(extract.find_urls(messege))

    return number_of_messeges, word_count, number_of_media_messeges, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100,
               2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messege'] != '<Media omitted>\n']

    f = open('stopwords.txt', 'r')
    stop_words = f.read()

    def rem_stop(messege):
        y = []
        for word in messege.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['messege'] = temp['messege'].apply(rem_stop)
    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    wc_img = wc.generate(temp['messege'].str.cat(sep=' '))
    return wc_img


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messege'] != '<Media omitted>\n']

    f = open('stopwords.txt', 'r')
    stop_words = f.read()
    words = []
    for messege in temp['messege']:
        for word in messege.lower().split():
            if word not in stop_words:
                if len(word) > 2:
                    words.append(word)
    ret_df = pd.DataFrame(Counter(words).most_common(20))
    return ret_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for messege in df['messege']:
        emojis.extend([c for c in messege if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()[
        'messege'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messege'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def monthly_activity_map(selected_user,  df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heat_map = df.pivot_table(
        index='day_name', columns='period', values='messege', aggfunc='count').fillna(0)

    return heat_map
