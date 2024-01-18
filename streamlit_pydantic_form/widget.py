__all__ = [
    "WidgetBuilder",
    "Slider",
    "Checkbox",
]
from abc import ABC, abstractmethod
from typing import Any

import streamlit as st


class WidgetBuilder(ABC):
    @abstractmethod
    def build(self) -> Any:
        ...


class Slider(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.slider(*self.args, **self.kwargs)


class Checkbox(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.checkbox(*self.args, **self.kwargs)
