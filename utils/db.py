"""Utilities for handling the database."""
import pymongo
import streamlit as st
import pandas as pd


class MongoHandler:
    """Class for handling the database.

    Parameters
    ----------
    set_project_name : str
        The name of the project that you are working on. It should be equal
        to the Rifa app.

    """
    NAME_COL = "NAME"
    PICKED_NUMBER_COL = "PICKED_NUMBER"
    PROJECT_COL = "PROJECT"

    def __init__(self, set_project_name: str):
        """Construct."""
        self.db = self.default_db()
        self.project = set_project_name

    @staticmethod
    def default_db():
        # Initialize connection.
        try:
            client = pymongo.MongoClient(**st.secrets["mongo"])
        except Exception as e:
            raise RuntimeError("Error with Mongo secrets.")
        db = client.test
        return db

    def delete_item(self, name: str) -> None:
        """Delete the first entry with provided NAME from the database."""
        self.db.my_collection.delete_one({
            MongoHandler.NAME_COL: name,
            MongoHandler.PROJECT_COL: self.project
        })

    def fetch_items(self) -> pd.DataFrame:
        """Fetch all documents for the given project as a DataFrame."""
        items = self.read_items()
        df = pd.DataFrame(items).drop(
            columns=["_id", MongoHandler.PROJECT_COL])
        return df

    def read_items(self):
        items = self.db.my_collection.find(
            filter={MongoHandler.PROJECT_COL: self.project})
        items = list(items)  # make hashable for st.cache
        return items

    def read_picked_numbers(self):
        """Fetch all documents from the database."""
        items = self.read_items()
        return [item[MongoHandler.PICKED_NUMBER_COL] for item in items]

    def write_new_item(
            self, name: str, num: int, kwargs: dict = {}):
        """Write a new document to the database.
        Parameters
        ----------
        name : str
            The name of the person.
        num : int
            The number that the person picked.
        kwargs : dict
            Additional key-value pairs to store.

        """
        capitalized_kwargs = {k.upper(): v for k, v in kwargs.items()}
        self.db.my_collection.insert_one({
            MongoHandler.NAME_COL: name,
            MongoHandler.PICKED_NUMBER_COL: num,
            MongoHandler.PROJECT_COL: self.project,
            **capitalized_kwargs
        })

    def remaining_numbers(self, total_numbers: int):
        """Return a list of numbers that have not been picked yet."""
        return list(
            set(range(1, total_numbers + 1)) -
            set(self.read_picked_numbers()))

    def nums_you_picked(self, your_name):
        """Return a list of numbers that you have already picked."""
        items = self.read_items()
        nums = [
            item[MongoHandler.PICKED_NUMBER_COL] for item in items
            if item[MongoHandler.NAME_COL].lower() == your_name.lower()]
        return nums
