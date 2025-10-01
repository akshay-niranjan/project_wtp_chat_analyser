import re
import pandas as pd

def preprocess(data):
    pattern2 = r"\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}"
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \s*\d{1,2}:\d{2}(?:\s?[apAP][mM])? -'

    message=re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    df=pd.DataFrame({'user_message':message,'message_date' : dates})
    df['message_date'] = df['message_date'].str.replace("\u202f", " ")  # Fix narrow space
    df['message_date'] = df['message_date'].str.replace(" -", "")  # Remove extra "-"
    df['message_date'] = df['message_date'].str.strip()

    df['message_date']=pd.to_datetime(df['message_date'],format="mixed")
    df.rename(columns={'message_date':'date'},inplace=True)

    # separate users and messages
    patt="([\w\W]+?):\s"
    users=[]
    messages=[]
    for message in df['user_message']:
        entry = re.split(patt,message)
        if entry[1:]: #user neame
           users.append(entry[1])
           messages.append(entry[2])
        else:
           users.append('group_notification')
           messages.append(entry[0])

    df['user']=users
    df['messages']=messages
    df.drop(columns=['user_message'],inplace=True)

    df['year']=df.date.dt.year
    df['month']=df.date.dt.month_name()
    df['month_num']=df.date.dt.month
    df['only_date']=df.date.dt.date
    df['day_name']=df.date.dt.day_name()
    df['day']=df.date.dt.day
    df['hour']=df.date.dt.hour
    df['minute']=df.date.dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
       if hour == 23:
           period.append(str(hour)+"-"+str('00'))
       elif hour == 0:
          period.append(str(00)+"-"+str(hour+1))
       else:
           period.append(str(hour)+"-"+str(hour+1))
        
    df['period']=period

    return df
