from pydantic import BaseModel
import streamlit as st
from typing import Self, Type, TypeVar, Generic


class WidgetFactory:
    ...


_T = TypeVar("_T", bound=BaseModel)


class st_auto_form(Generic[_T]):
    def __init__(
        self,
        key: str,
        *,
        model: Type[_T],
        clear_on_submit: bool = False,
        border: bool = True,
    ) -> None:
        self.key = key
        self.model = model
        self.clear_on_submit = clear_on_submit
        self.border = border
        self.form = st.form(key=self.key, clear_on_submit=self.clear_on_submit)

    def input_components(self) -> _T:
        # TODO: No components for now
        return self.model()

    def __enter__(self) -> Self:
        # Enter the inner st.form
        self.form.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Exit the inner st.form
        self.form.__exit__(exc_type, exc_value, traceback)
