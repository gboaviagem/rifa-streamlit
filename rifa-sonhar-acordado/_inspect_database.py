"""Fetch all documents from the database and export as csv."""
import streamlit as st
import time
from utils.db import MongoHandler

# Initialize connection.
db = MongoHandler()

st.title("Displaying the current numbers in the database.")

with st.spinner('Reading from the database...'):
    df = db.fetch_numbers()

df = df.query("NAME != '__None__'")
st.dataframe(df)

@st.dialog("Erasing...")
def erase_db():
    items = db.read_items()
    with st.spinner("Erasing all items..."):
        for item in items:
            db.delete_item(name=item['NAME'])

st.text("What do you wish to do?")
st.button("Erase database", on_click=erase_db)
