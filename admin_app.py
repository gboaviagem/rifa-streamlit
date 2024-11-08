"""Fetch all documents from the database and export as csv."""
import streamlit as st
from utils.db import MongoHandler

project = st.text_input("Project name:")
if not project:
    st.stop()
# Initialize connection.
db = MongoHandler(set_project_name=project)

st.title("Displaying the current numbers in the database.")

with st.spinner('Reading from the database...'):
    df = db.fetch_numbers()

st.dataframe(df)

@st.dialog("Erasing...")
def erase_db():
    items = db.read_items()
    with st.spinner("Erasing all items..."):
        for item in items:
            db.delete_item(name=item[MongoHandler.NAME_COL])

def write_db():
    filename = "rifa_project_data.csv"
    df.to_csv(filename, index=False)
    st.success(f"CSV written to file {filename}!")

st.text("What do you wish to do?")

st.button("Erase database", on_click=erase_db)
st.button("Write database to CSV", on_click=write_db)
