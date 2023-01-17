import pandas
import streamlit as st
import database

def review():
    with st.form("Review an event"):
        userId = st.text_input("userId", value = "0")
        events = database.get_all_events()
        eventIndexList = [*range(len(events))]
        eventIndex = st.selectbox("Event", eventIndexList, format_func=lambda x: events[x][0])
        eventId = events[eventIndex][6]
        rating = st.number_input("Rate the event",min_value=1, max_value=5, value=3, step=1)
        review = st.text_area("Write your review", value="")
        if st.form_submit_button("Enter"):
            database.add_review(userId, eventId, rating, review)
            st.success("review submitted")
