import warnings
from types import TracebackType
from typing import Any, Generic, Self, TypeVar

import streamlit as st
from pydantic import BaseModel
from typing_extensions import deprecated

from .widget import WidgetBuilder

_T = TypeVar("_T", bound=BaseModel)


class st_auto_form(Generic[_T]):  # noqa: N801
    def __init__(
        self,
        key: str,
        *,
        model: type[_T],
        clear_on_submit: bool = False,
        border: bool = True,
        widget_builder: WidgetBuilder | None = None,
    ) -> None:
        self.key = key
        self.model = model
        self.clear_on_submit = clear_on_submit
        self.border = border
        self.form = st.form(key=self.key, clear_on_submit=self.clear_on_submit)
        self.widget_builder = widget_builder

    def input_widgets(self) -> _T:
        if self.widget_builder is not None:
            return self.widget_builder.build()
        return _model_to_input_components(self.model)

    @deprecated(
        "st_auto_form.input_components() is deprecated, use st_auto_form.input_widgets() instead",
    )
    def input_components(self) -> _T:
        warnings.warn(
            "st_auto_form.input_components() is deprecated, use st_auto_form.input_widgets() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.input_widgets()

    def __enter__(self) -> Self:
        # Enter the inner st.form
        self.form.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        # Exit the inner st.form
        self.form.__exit__(exc_type, exc_value, traceback)


class NoWidgetBuilderFoundError(Exception):
    pass


def _extract_widget_builder_from_metadata(metadata: list[Any]) -> WidgetBuilder:
    try:
        return next(item for item in metadata if isinstance(item, WidgetBuilder))
    except StopIteration as e:
        msg = "No widget builder found in metadata"
        raise NoWidgetBuilderFoundError(msg) from e


def _model_to_input_components(model: type[_T]) -> _T:
    raw_input_values = {}
    for name, field in model.model_fields.items():
        try:
            raw_input_values[name] = _extract_widget_builder_from_metadata(
                field.metadata,
            ).build()
        except NoWidgetBuilderFoundError:
            if field.annotation is None:
                raise
            if issubclass(field.annotation, BaseModel):
                raw_input_values[name] = _model_to_input_components(field.annotation)
            else:
                raise

    return model(**raw_input_values)
