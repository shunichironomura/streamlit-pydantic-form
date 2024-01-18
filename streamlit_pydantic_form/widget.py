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


# Widget builders for Streamlit input widgets
# Note "st.button and st.download_button cannot be added to a form."
# Ref: https://docs.streamlit.io/library/api-reference/control-flow/st.form


class Checkbox(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.checkbox(*self.args, **self.kwargs)


class Toggle(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.toggle(*self.args, **self.kwargs)


class Radio(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.radio(*self.args, **self.kwargs)


class Selectbox(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.selectbox(*self.args, **self.kwargs)


class Multiselect(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.multiselect(*self.args, **self.kwargs)


class Slider(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.slider(*self.args, **self.kwargs)


class SelectSlider(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.select_slider(*self.args, **self.kwargs)


class TextInput(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.text_input(*self.args, **self.kwargs)


class NumberInput(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.number_input(*self.args, **self.kwargs)


class TextArea(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.text_area(*self.args, **self.kwargs)


class DateInput(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.date_input(*self.args, **self.kwargs)


class TimeInput(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.time_input(*self.args, **self.kwargs)


class FileUploader(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.file_uploader(*self.args, **self.kwargs)


class CameraInput(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.camera_input(*self.args, **self.kwargs)


class ColorPicker(WidgetBuilder):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return st.color_picker(*self.args, **self.kwargs)
