import streamlit as st
import matplotlib.pyplot as plt

import preproccessor, helper
st.sidebar.title("Whatsapp chat analyzer")

#to upload file
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    #convert to string
    data= bytes_data.decode("utf-8")
    df=preproccessor.preprocess(data)
    # st.dataframe(df)

    #fetch unique users
    user_lists=df['user'].unique().tolist()
    #remove group_notification
    user_lists.remove('group_notification')
    #sort user list
    user_lists.sort()
    user_lists.insert(0,'Overall')

    #show user list
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_lists)

    #add button
    if st.sidebar.button("Show Analysis"):
        #in helper file we have function fetch_stats we are using it to get number of messages
        num_message, words, num_media_msg=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        #divide into three columns
        col1, col2, col3 = st.columns(3)

        #column1 for total number of messages of particular user
        with col1:
            st.header('Total messages')
            st.title(num_message)
        with col2:
            st.header('Total number of words')
            st.title(words)
        with col3:
            st.header('Number of media items')
            st.title(num_media_msg)

#finding the busiest user in the group
        if selected_user == 'Overall':
            st.title('Most Busy User')
            x, new_df = helper.most_busy_user(df)

            fig, ax = plt.subplots()  # corrected syntax
            ax.barh(x.index, x.values, color='green')  # corrected to x.values

            col3, col4 = st.columns(2)
            with col3:
                st.pyplot(fig)

            with col4:
                st.dataframe(new_df)

    #word_cloud
    st.title('Word Cloud')
    df_wc=helper.create_wordscloud( selected_user,df)
    fig1, ax1=plt.subplots()
    ax1.imshow(df_wc)
    st.pyplot(fig1)

    #most common words
    most_common_df=helper.most_common_words( selected_user,df)
    fig2, ax2=plt.subplots()
    ax2.barh(most_common_df[0],most_common_df[1])
    st.title('Most common words')
    st.pyplot(fig2)

    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")
    col4, col5 = st.columns(2)

    with col4:
        st.dataframe(emoji_df)
    with col5:
        fig, ax = plt.subplots()
        ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(),autopct="%0.2f")
        st.pyplot(fig)

    #timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user,df)
    fig, ax=plt.subplots()
    ax.plot(timeline['time'], timeline['messages'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    #daily timeline
    st.title("Daily Timeline")
    daily_timeline=helper.daily_timeline(selected_user,df)
    fig, ax=plt.subplots()
    ax.plot(daily_timeline['onlyDate'], daily_timeline['messages'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Title for the Streamlit app
    st.title('Busiest day of the week')

    # Getting the busiest day data
    weekly_timeline = helper.busiest_day(selected_user, df)

    # Convert index and values to appropriate types
    days = weekly_timeline.index.astype(str).tolist()
    counts = weekly_timeline.values.astype(int).tolist()

    # Plotting the data
    fig, ax = plt.subplots()
    ax.bar(days, counts)

    # Adding labels and title to the plot
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Message Count')
    ax.set_title('Message Count by Day of the Week')

    # Rotating x-ticks for better readability
    plt.xticks(rotation='vertical')

    # Adjusting the layout
    plt.tight_layout()

    # Displaying the plot in Streamlit
    st.pyplot(fig)

    # Title for the Streamlit app
    st.title('Busiest month')

    # Getting the busiest day data
    weekly_timeline = helper.busiest_month(selected_user, df)

    # Convert index and values to appropriate types
    days = weekly_timeline.index.astype(str).tolist()
    counts = weekly_timeline.values.astype(int).tolist()
    fig, ax = plt.subplots()
    ax.bar(days, counts)

    # Adding labels and title to the plot
    ax.set_xlabel('Month name')
    ax.set_ylabel('Message Count')
    ax.set_title('Message Count by Month')

    # Rotating x-ticks for better readability
    plt.xticks(rotation='vertical')

    # Adjusting the layout
    plt.tight_layout()

    # Displaying the plot in Streamlit
    st.pyplot(fig)
