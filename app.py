# Importing pakages
import pandas as pd
import streamlit as st
import mysql.connector
import events
import bookings
import review
import organiser
import user
import database
import venue

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="H@rd.Study123$"
)
c = mydb.cursor()

# c.execute("CREATE DATABASE TRAINS")


def main():
    st.title("Event Booking App")
    menu = ["Events","Bookings", "review event", "add or renew event", "view org bookings", "any query", "New user", "New venue", "Delete event"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Events":
        st.subheader("Events")
        events.read()

    elif choice == "Bookings":
        st.subheader("Book an event")
        bookings.create_1()
        st.markdown("---")
        bookings.viewBookings()

    elif choice == "review event":
        st.subheader("Review an event")
        review.review()

    elif choice == "add or renew event":
        st.subheader("Add or Renew Events (Organizer view)")
        organiser.addEvent()
        st.markdown("---")
        organiser.addTags()
        st.markdown("---")
        organiser.renewEvent()
        st.markdown("---")
        organiser.edit_event()

    elif choice == "view org bookings":
        st.subheader("View Bookings for your events")
        OrgId = st.text_input("Organiser Id")
        if st.button("go"):
            organiser.getOrgBookings(OrgId)

    elif choice == "any query":
        st.subheader("enter any query")
        query = st.text_input("query:")
        result = database.run_query(query)
        df = pd.DataFrame(result)
        st.dataframe(df)

    elif choice == "New user":
        st.subheader("Register")
        user.newUser()

    elif choice == "New venue":
        st.subheader("Add a Venue")
        venue.add_venue()

    elif choice == "Delete event":
        st.subheader("Delete event")
        organiser.delete_event()





if __name__ == '__main__':
    main()