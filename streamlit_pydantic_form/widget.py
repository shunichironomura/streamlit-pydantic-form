from abc import ABC, abstractmethod
from typing import Any

import streamlit as st


class WidgetBuilder(ABC):
    @abstractmethod
    def build(self) -> Any:
        ...


class slider(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.slider(*self.args, **self.kwargs)


class checkbox(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.checkbox(*self.args, **self.kwargs)
