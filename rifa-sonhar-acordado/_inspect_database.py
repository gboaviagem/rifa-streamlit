"""Fetch all documents from the database and export as csv."""
import streamlit as st
from utils.db import MongoHandler

# Initialize connection.
db = MongoHandler()

st.title("Displaying the current numbers in the database.")

with st.spinner('Reading from the database...'):
    df = db.fetch_numbers()

df = df.query("NAME != '__None__'")
st.dataframe(df)
