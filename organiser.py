import pandas
import streamlit as st
import database
import datetime
import plotly.express as px
def addEvent():
    st.text("Add Event")
    with st.form("Add event"):
        OrgId = st.text_input("Organiser Id")
        eventName = st.text_input("Enter the event Name", max_chars=50)
        eventDate = (st.date_input("Enter event date", min_value=datetime.date.today())).strftime("%Y-%m-%d")
        eventTime = (st.time_input("Enter event time")).strftime("%H:%M:%S")
        eventDate=eventDate+" "+eventTime
        seatPrice = st.number_input("Enter price", min_value=0.0, value=0.0, step=0.01)
        seatAvailable = st.number_input("Enter number of seats", min_value=0, value=0, step = 1)
        Details = st.text_area("Enter event details")
        venues = database.get_venues()
        venueIndexList = [*range(len(venues))]
        venueIndex = st.selectbox("Venues", venueIndexList, format_func=lambda x: venues[x][1] + "Address: "+ venues[x][2])
        venueId = venues[venueIndex][0]
        AgeOfEntry = st.number_input("Enter age limit (Leave 0 for none)", min_value=0, step=1, value=0)


        if st.form_submit_button("Add"):
            database.add_event(eventName, eventDate, seatPrice, seatAvailable, Details, OrgId, venueId, int(AgeOfEntry))
            st.success("Added successfully")

def addTags():
    st.text("Add Tags")
    OrgId = st.text_input("Organiser Id", value="1", key = 122)
    events = database.get_events_by_Org(OrgId)
    eventIndexList = [*range(len(events))]
    eventIndex = st.selectbox("Event", eventIndexList, format_func=lambda x: events[x][0])
    eventId = events[eventIndex][6]

    tagNameList = database.get_tags()
    tagIndexList = [*range(len(tagNameList))]
    tagsIndex = st.multiselect("Enter Event Tags", tagIndexList, format_func=lambda x:tagNameList[x][0])
    tags = [tagNameList[x][1] for x in tagsIndex]
    if st.button("Add"):
        database.add_tags(eventId, tags)
        st.success("Tags Added")


def renewEvent():
    st.text("Renew Event")
    OrgId = st.text_input("Organiser Id", value =0, key = 111)
    events = database.get_inactive_events(OrgId)
    if(not events):
        st.text("No events to renew")
    else:
        with st.form("Renew Event"):
            eventIndexList = [*range(len(events))]
            eventIndex = st.selectbox("Event", eventIndexList, format_func=lambda x: str(events[x][0])+":"+str(events[x][1]))
            eventId = events[eventIndex][0]
            newDate = (st.date_input("Event Date", min_value=datetime.date.today())).strftime("%Y-%m-%d")

            if st.form_submit_button("Renew"):
                database.renew_event(eventId, newDate)

def getOrgBookings(OrgId):
    st.text("Get Bookings for your events")
    Bookings = database.get_bookings_by_org(OrgId)
    df = pandas.DataFrame(Bookings, columns=['Event ID', 'Total Seats', 'Total Revenue'])
    with st.expander("Bookings for your events"):
        p1 = px.pie(df, values="Total Revenue", names="Event ID")
        st.dataframe(df)
        st.plotly_chart(p1)

def edit_event():
    st.text("Edit Event")

    OrgId = st.text_input("Organiser Id", value="0", key=123)
    events = database.get_events_by_Org(OrgId)
    eventIndexList = [*range(len(events))]
    eventIndex = st.selectbox("Event", eventIndexList, format_func=lambda x: events[x][0], key=897)
    eventId = events[eventIndex][6]
    with st.form("Update this event"):
        eventName = st.text_input("Update the event Name", max_chars=50)
        eventDate = (st.date_input("Update event date", min_value=datetime.date.today())).strftime("%Y-%m-%d")
        eventTime = (st.time_input("Update event time")).strftime("%H:%M:%S")
        eventDate = eventDate + " " + eventTime
        seatPrice = st.number_input("Update price", min_value=0.0, value=0.0, step=0.01)
        seatAvailable = st.number_input("Update number of seats", min_value=0, value=0, step=1)
        Details = st.text_area("Update event details")
        venues = database.get_venues()
        venueIndexList = [*range(len(venues))]
        venueIndex = st.selectbox("Venues", venueIndexList, format_func=lambda x: venues[x][1] + "Address: " + venues[x][2], key="12312")
        venueId = venues[venueIndex][0]
        AgeOfEntry = st.number_input("Update age limit (Leave 0 for none)", min_value=0, step=1, value=0)
        Status = st.checkbox("Is Event Active?: ", value=True)
        Status = 1 if Status else 0
        if st.form_submit_button("Update"):
            database.update_event(eventId, eventName, eventDate, seatPrice, seatAvailable, Details, OrgId, venueId, int(AgeOfEntry), Status)
            st.success("event successfully updated")

def delete_event():
    st.text("Delete Event")

    OrgId = st.text_input("Organiser Id", value="1", key=123)
    events = database.get_events_by_Org(OrgId)
    eventIndexList = [*range(len(events))]
    eventIndex = st.selectbox("Event", eventIndexList, format_func=lambda x: events[x][0], key=897)
    eventId = events[eventIndex][6]
    if st.button("Delete event"):
        database.delete_event(eventId)

"""def add_organiser():
    name = st.text_input("Organiser name")
    if st.button("add"):
        database.add_organiser(name)
        st.success("added")"""