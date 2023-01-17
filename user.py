import streamlit as st
import database
import datetime
def newUser():
    birth = datetime.date(1922,1,1)
    with st.form("Enter your details"):
        username = st.text_input("Enter your name")
        dob = st.date_input("Enter your date of birth", min_value=birth)
        dob=dob.strftime("%Y-%m-%d")

        if st.form_submit_button("Create Account"):
            database.add_user(username, dob)
            st.success("Account created")