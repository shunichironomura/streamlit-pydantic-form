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

_NOT_SET = object()


class WidgetBuilder(ABC, Generic[_T]):
    default = _NOT_SET

    @abstractmethod
    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: _T | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> _T: ...


# Widget builders for Streamlit input widgets
# Note "st.button and st.download_button cannot be added to a form."
# Ref: https://docs.streamlit.io/library/api-reference/control-flow/st.form


def _generate_random_key() -> str:
    return str(uuid4())


class Checkbox(WidgetBuilder[bool]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: bool = False

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: bool | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> bool:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.checkbox(*self._args, **kwargs) if form is None else form.checkbox(*self._args, **kwargs)


class Toggle(WidgetBuilder[bool]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: bool = False

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: bool | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> bool:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.toggle(*self._args, **kwargs) if form is None else form.toggle(*self._args, **kwargs)


class Radio(WidgetBuilder[Any | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: int | None = 0

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: Any | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> Any | None:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"index": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.radio(*self._args, **kwargs) if form is None else form.radio(*self._args, **kwargs)


class Selectbox(WidgetBuilder[Any | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: int | None = 0

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: Any | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> Any | None:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"index": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.selectbox(*self._args, **kwargs) if form is None else form.selectbox(*self._args, **kwargs)


class Multiselect(WidgetBuilder[list[Any]]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: Any | None = None

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: list[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> list[Any]:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"default": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.multiselect(*self._args, **kwargs) if form is None else form.multiselect(*self._args, **kwargs)


class Slider(WidgetBuilder[Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: Any | None = None

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: Any | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> Any:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.slider(*self._args, **kwargs) if form is None else form.slider(*self._args, **kwargs)


class SelectSlider(WidgetBuilder[Any | tuple[Any]]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default = None

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: Any | tuple[Any] | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> Any | tuple[Any]:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.select_slider(*self._args, **kwargs) if form is None else form.select_slider(*self._args, **kwargs)


class TextInput(WidgetBuilder[str | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: str = ""

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: str | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> str | None:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.text_input(*self._args, **kwargs) if form is None else form.text_input(*self._args, **kwargs)  # type: ignore[no-any-return]


class NumberInput(WidgetBuilder[int | float | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: int | float | Literal["min"] = "min"

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: float | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> int | float | None:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default  # type: ignore[assignment] # TODO: Fix this
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.number_input(*self._args, **kwargs) if form is None else form.number_input(*self._args, **kwargs)  # type: ignore[no-any-return]


class TextArea(WidgetBuilder[str | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: str = ""

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: str | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> str | None:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.text_area(*self._args, **kwargs) if form is None else form.text_area(*self._args, **kwargs)  # type: ignore[no-any-return]


class DateInput(WidgetBuilder[DateWidgetReturn]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: DateValue | Literal["today"] = "today"

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: DateWidgetReturn | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> DateWidgetReturn:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default  # type: ignore[assignment] # TODO: Fix this
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.date_input(*self._args, **kwargs) if form is None else form.date_input(*self._args, **kwargs)


class TimeInput(WidgetBuilder[time | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: time | datetime | Literal["now"] = "now"

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: time | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> time | None:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default  # type: ignore[assignment] # TODO: Fix this
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.time_input(*self._args, **kwargs) if form is None else form.time_input(*self._args, **kwargs)  # type: ignore[no-any-return]


class FileUploader(WidgetBuilder[Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: Any | None = None,  # noqa: ARG002
        kwargs: dict[str, Any] | None = None,
    ) -> Any:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.file_uploader(*self._args, **kwargs) if form is None else form.file_uploader(*self._args, **kwargs)


class CameraInput(WidgetBuilder[UploadedFile | None]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: UploadedFile | None = None,  # noqa: ARG002
        kwargs: dict[str, Any] | None = None,
    ) -> UploadedFile | None:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.camera_input(*self._args, **kwargs) if form is None else form.camera_input(*self._args, **kwargs)


class ColorPicker(WidgetBuilder[str]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._args = args
        self._kwargs = kwargs
        self.default: str | None = None

    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,
        value: str | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> str:
        kwargs = self._kwargs | kwargs if kwargs is not None else self._kwargs
        value = value if value is not None else self.default
        kwargs = kwargs | {"value": value}
        if randomize_key:
            kwargs["key"] = _generate_random_key()
        return st.color_picker(*self._args, **kwargs) if form is None else form.color_picker(*self._args, **kwargs)
