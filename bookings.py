import pandas
import streamlit as st
import database
import random

def create_1():
    with st.form("Book tickets"):
        userId = st.text_input("userId")
        events = database.get_all_events()
        eventIndexList = [*range(len(events))]
        eventIndex = st.selectbox("Event",eventIndexList, format_func=lambda x: events[x][0])
        eventId = events[eventIndex][6]
        seatsAvailable = events[eventIndex][7]
        if(seatsAvailable==0):
            st.text("Out of seats")
        st.text("Available seats: "+ str(seatsAvailable))
        seats = st.number_input("Seats", min_value=0, max_value=int(seatsAvailable), value=0, step=1)
        submitButton = st.form_submit_button("Book Tickets")
        if submitButton:
                TransactionId = random.randint(100000000000, 999999999999)
                result = database.book_event(TransactionId, seats, userId, eventId)
                if result:
                    st.success("Tickets successfully booked")
                else:
                    st.success("Ticket booking failed")

def viewBookings():
    userId = st.text_input("userId", value = "0")
    result = database.get_user_bookings(userId)
    df = pandas.DataFrame(result, columns=['bookingId', 'eventName', 'Seats'])
    with st.expander("View your bookings"):
        st.dataframe(df)
