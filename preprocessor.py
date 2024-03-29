import re
import pandas as pd


def preprocess(data):

    pattern = '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s'
    messeges = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_messege': messeges, 'messege_date': dates})
    df['messege_date'] = pd.to_datetime(
        df['messege_date'], format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'messege_date': 'date'}, inplace=True)
    users = []
    messeges = []
    for messege in df['user_messege']:
        entry = re.split('([\w\W]+?):\s', messege)
        if entry[1:]:
            users.append(entry[1])
            messeges.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messeges.append(entry[0])

    df['user'] = users
    df['messege'] = messeges
    df.drop(columns=['user_messege'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
