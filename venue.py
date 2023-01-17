import streamlit as st
import database

def add_venue():
    with st.form("Enter data"):
        Name = st.text_input("Enter name of venue")
        Address = st.text_area("Enter address")

        if st.form_submit_button("Add"):
            database.add_venue(Name, Address)
            st.success("Added")
