import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper


st.sidebar.title('Whatsapp Chat Analyser')

# File uploader

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")      # converting byte data to string
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    # fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        num_msg,num_words,num_media_msg,num_links=helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_msg)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
    
    # Monthly Timeline
    st.title("Monthly Timeline")
    timeline=helper.monthly_timeline(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(timeline.time,timeline.messages,color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Daily Timeline
    st.title("Daily Timeline")
    daily_timeline=helper.daily_timeline(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(daily_timeline.only_date,daily_timeline.messages,color='grey')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Activity map
    st.title('Activity Map')
    col1,col2=st.columns(2)
    with col1:
        st.header("Most Busy Day")
        busy_day=helper.week_activity_map(selected_user,df)
        fig,ax=plt.subplots()
        plt.bar(busy_day.index,busy_day.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        busy_month=helper.month_activity_map(selected_user,df)
        fig,ax=plt.subplots()
        plt.bar(busy_month.index,busy_month.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # Activity Heatmap
    st.title("Weekly Activity HeatMap")
    user_heatmap=helper.activity_heatmap(selected_user,df)
    fig,ax=plt.subplots()
    ax=sns.heatmap(user_heatmap)
    st.pyplot(fig)


    # Graph
    if selected_user == 'Overall' or selected_user != 'Overall':
        x,new_df=helper.most_busy_users(df)
        fig,ax=plt.subplots()

        col1,col2=st.columns(2)
        with col1:
            st.title('Most Busy Users')
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title('Percentage wise')
            st.dataframe(new_df)
    
    # wordcloud
    st.title('WordCloud-Most used words')
    df_wc=helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # most common words
    return_df=helper.most_common_words(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(return_df[0],return_df[1],color='violet')
    plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)

    # EMOJI
    st.title("Emoji Analysis")
    emoji_df=helper.emoji_helper(selected_user,df)

    col1,col2=st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1],labels=emoji_df[0],autopct='%0.2f',textprops={'fontsize': 14, 'fontname': 'Segoe UI Emoji'})
        st.pyplot(fig)
    

st.sidebar.title('Steps to Export Whatsapp Chat')
st.sidebar.write('1.Go to your chat')
st.sidebar.write('2.click on 3 dots')
st.sidebar.write('3.More-export chat-without media')
