import time
from collections.abc import Callable, Generator

import streamlit as st

from utils.i18n import i18n


# [Files]
def read_file_content(file_path: str) -> str:
    """
    Read and return the content of a text file.

    Arguments:
        file_path (str): Path to the file to be read

    Returns:
        str: Content of the file as a string
    """
    with open(file_path, encoding="utf-8") as file:
        file_content = file.read()
    return file_content


# [Badges]
def info_badge(msg: str) -> str:
    """
    Generate an info badge message.

    Arguments:
        msg (str): The message to display in the badge

    Returns:
        str: The formatted info badge message
    """
    return f"\n:blue-badge[:material/info: {msg}]\n\n"


def success_badge(msg: str) -> str:
    """
    Generate a success badge message.

    Arguments:
        msg (str): The message to display in the badge

    Returns:
        str: The formatted success badge message
    """
    return f"\n:green-badge[:material/check: {msg}]\n\n"


def error_badge(msg: str) -> str:
    """
    Generate an error badge message.

    Arguments:
        msg (str): The message to display in the badge

    Returns:
        str: The formatted error badge message
    """
    return f"\n:red-badge[:material/error: {msg}]\n\n"


# [Streamlit]
class st_spinner:
    # ref: https://github.com/streamlit/streamlit/issues/6799#issuecomment-1578395288
    def __init__(self, text=i18n("spinner.loading"), show_time=True):
        self.text = text
        self.show_time = show_time
        self._spinner = iter(self._start())  # This creates an infinite spinner
        next(self._spinner)  #  This starts it

    def _start(self):
        with st.spinner(self.text, show_time=self.show_time):
            yield

    def end(self):  # This ends it
        next(self._spinner, None)


# # Usage
# s = st_spinner()
# time.sleep(5)
# s.end()


# [IO]
def str_stream(text: str) -> Generator:
    """
    Stream the provided text by yielding one character at a time with a brief delay
    to simulate typing.

    Arguments:
        text (str): Text to stream character by character

    Yields:
        str: Individual characters of the text
    """
    for char in text:
        yield char
        time.sleep(0.005)


# [General]
color_map = {
    0: "blue",
    1: "green",
    2: "red",
    3: "purple",
    4: "orange",
    5: "pink",
    6: "brown",
    7: "gray",
    8: "cyan",
    9: "magenta",
    10: "lime",
    11: "teal",
    12: "navy",
    13: "maroon",
    14: "olive",
    15: "coral",
    16: "salmon",
    17: "gold",
    18: "khaki",
    19: "plum",
}


# [Decorators]
def mock_return(result):
    def Inner(func):
        def wrapper(*args, **kwargs):
            if isinstance(result, Callable):
                return result(*args, **kwargs)
            else:
                return result

        return wrapper

    return Inner
