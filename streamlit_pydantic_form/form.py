from typing import Any, Generic, Self, TypeVar

import streamlit as st
from pydantic import BaseModel

from .widget import WidgetBuilder

_T = TypeVar("_T", bound=BaseModel)


class st_auto_form(Generic[_T]):
    def __init__(
        self,
        key: str,
        *,
        model: type[_T],
        clear_on_submit: bool = False,
        border: bool = True,
    ) -> None:
        self.key = key
        self.model = model
        self.clear_on_submit = clear_on_submit
        self.border = border
        self.form = st.form(key=self.key, clear_on_submit=self.clear_on_submit)

    def input_components(self) -> _T:
        raw_input_values = {}
        for name, field in self.model.model_fields.items():
            raw_input_values[name] = _extract_widget_builder_from_metadata(
                field.metadata,
            ).build()
        return self.model(**raw_input_values)

    def __enter__(self) -> Self:
        # Enter the inner st.form
        self.form.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Exit the inner st.form
        self.form.__exit__(exc_type, exc_value, traceback)


class NoWidgetBuilderFoundError(Exception):
    pass


def _extract_widget_builder_from_metadata(metadata: list[Any]) -> WidgetBuilder:
    try:
        return next(item for item in metadata if isinstance(item, WidgetBuilder))
    except StopIteration:
        raise NoWidgetBuilderFoundError("No widget builder found in metadata")
