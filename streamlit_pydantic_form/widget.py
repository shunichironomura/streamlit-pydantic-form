__all__ = [
    "WidgetBuilder",
    "Slider",
    "Checkbox",
]
from abc import ABC, abstractmethod
from datetime import datetime, time
from typing import Any, Generic, Literal, TypeVar
from uuid import uuid4

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit.elements.widgets.time_widgets import DateValue, DateWidgetReturn
from streamlit.runtime.uploaded_file_manager import UploadedFile

_T = TypeVar("_T")

_DEFAULT_NOT_SET = object()


class WidgetBuilder(ABC, Generic[_T]):
    default = _DEFAULT_NOT_SET

    @abstractmethod
    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> _T: ...


# Widget builders for Streamlit input widgets
# Note "st.button and st.download_button cannot be added to a form."
# Ref: https://docs.streamlit.io/library/api-reference/control-flow/st.form


def _generate_random_key() -> str:
    return str(uuid4())


class Checkbox(WidgetBuilder[bool]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: bool = False

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> bool:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.checkbox(*self.args, **kwargs) if form is None else form.checkbox(*self.args, **kwargs)


class Toggle(WidgetBuilder[bool]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: bool = False

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> bool:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.toggle(*self.args, **kwargs) if form is None else form.toggle(*self.args, **kwargs)


class Radio(WidgetBuilder[Any | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: int | None = 0

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> Any | None:
        kwargs = self.kwargs | {"index": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.radio(*self.args, **kwargs) if form is None else form.radio(*self.args, **kwargs)


class Selectbox(WidgetBuilder[Any | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: int | None = 0

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> Any | None:
        kwargs = self.kwargs | {"index": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.selectbox(*self.args, **kwargs) if form is None else form.selectbox(*self.args, **kwargs)


class Multiselect(WidgetBuilder[list[Any]]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: Any | None = None

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> list[Any]:
        kwargs = self.kwargs | {"default": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.multiselect(*self.args, **kwargs) if form is None else form.multiselect(*self.args, **kwargs)


class Slider(WidgetBuilder[Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: Any | None = None

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> Any:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.slider(*self.args, **kwargs) if form is None else form.slider(*self.args, **kwargs)


class SelectSlider(WidgetBuilder[Any | tuple[Any]]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default = None

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> Any | tuple[Any]:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.select_slider(*self.args, **kwargs) if form is None else form.select_slider(*self.args, **kwargs)


class TextInput(WidgetBuilder[str | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: str = ""

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> str | None:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.text_input(*self.args, **kwargs) if form is None else form.text_input(*self.args, **kwargs)  # type: ignore[no-any-return]


class NumberInput(WidgetBuilder[int | float | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: int | float | Literal["min"] = "min"

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> int | float | None:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.number_input(*self.args, **kwargs) if form is None else form.number_input(*self.args, **kwargs)  # type: ignore[no-any-return]


class TextArea(WidgetBuilder[str | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: str = ""

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> str | None:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.text_area(*self.args, **kwargs) if form is None else form.text_area(*self.args, **kwargs)  # type: ignore[no-any-return]


class DateInput(WidgetBuilder[DateWidgetReturn]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: DateValue | Literal["today"] = "today"

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> DateWidgetReturn:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.date_input(*self.args, **kwargs) if form is None else form.date_input(*self.args, **kwargs)


class TimeInput(WidgetBuilder[time | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: time | datetime | Literal["now"] = "now"

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> time | None:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.time_input(*self.args, **kwargs) if form is None else form.time_input(*self.args, **kwargs)  # type: ignore[no-any-return]


class FileUploader(WidgetBuilder[Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> Any:
        kwargs = self.kwargs.copy()
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.file_uploader(*self.args, **kwargs) if form is None else form.file_uploader(*self.args, **kwargs)


class CameraInput(WidgetBuilder[UploadedFile | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> UploadedFile | None:
        kwargs = self.kwargs.copy()
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.camera_input(*self.args, **kwargs) if form is None else form.camera_input(*self.args, **kwargs)


class ColorPicker(WidgetBuilder[str]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self.default: str | None = None

    def build(self, form: DeltaGenerator | None = None, *, randomize_key: bool = False) -> str:
        kwargs = self.kwargs | {"value": self.default}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.color_picker(*self.args, **kwargs) if form is None else form.color_picker(*self.args, **kwargs)
