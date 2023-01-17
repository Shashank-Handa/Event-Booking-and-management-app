import pandas as pd
import streamlit as st
import database
import datetime
def read():
    result = database.get_events_by_rating()
    df = pd.DataFrame(result, columns=['eventName', 'eventDate', 'Age_of_entry', 'Details', 'OrgName', 'VenueName'])
    with st.expander("View All Events"):
        st.dataframe(df)

    #get events by tag
    tagNameList = database.get_tags()
    tagNames=[x[0] for x in tagNameList]
    option = st.selectbox("Select Tags", tagNames)
    result2 = database.get_events_by_tag(option)
    df2 = pd.DataFrame(result2, columns=['eventName', 'eventDate', 'Age_of_entry', 'Details', 'OrgName', 'VenueName', 'eventId', 'seatsAvailable'])
    with st.expander("Get Events by Tag"):
        st.dataframe(df2)

    #get events by date:
    d1=st.date_input("See events From", min_value=datetime.date.today())
    d2=st.date_input("See events to", min_value=d1, value=d1+datetime.timedelta(days=1))
    result3=database.get_events_by_date(d1.strftime("%Y-%m-%d"), d2.strftime("%Y-%m-%d"))
    df3 = pd.DataFrame(result3, columns=['eventName', 'eventDate', 'Age_of_entry', 'Details', 'OrgName', 'VenueName', 'eventId', 'seatsAvailable'])
    with st.expander("Get events by date"):
        st.dataframe(df3)

"""def recommendedEvents():
    userId = st.text_input("Enter user id", value="2")
    result=database.get_recommendation(userId)
    df = pd.DataFrame(result,
                 columns=['eventName', 'eventDate', 'Age_of_entry', 'Details', 'OrgName', 'VenueName', 'eventId',
                          'seatsAvailable'])
    with st.expander("Recommended events"):
        st.dataframe(df)"""


