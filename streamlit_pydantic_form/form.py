import warnings
from inspect import isclass
from types import GenericAlias, TracebackType
from typing import Any, Generic, Self, TypeVar, get_args, get_origin

import streamlit as st
from pydantic import BaseModel
from pydantic_core import PydanticUndefined
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
        widget_builder: WidgetBuilder[_T] | None = None,
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


def _extract_widget_builder_from_metadata(metadata: list[Any]) -> WidgetBuilder[Any]:
    try:
        return next(item for item in metadata if isinstance(item, WidgetBuilder))
    except StopIteration as e:
        msg = "No widget builder found in metadata"
        raise NoWidgetBuilderFoundError(msg) from e


_SUPPORTED_GENERIC_ALIAS = {list}


def _model_to_input_components(model: type[_T]) -> _T:
    raw_input_values = {}
    for name, field in model.model_fields.items():
        try:
            builder = _extract_widget_builder_from_metadata(field.metadata)
            if field.default is not PydanticUndefined:
                builder.default = field.default
            raw_input_values[name] = builder.build()
        except NoWidgetBuilderFoundError:
            if field.annotation is None:
                raise
            if (
                isinstance(field.annotation, GenericAlias)
                and (origin := get_origin(field.annotation)) in _SUPPORTED_GENERIC_ALIAS
            ):
                st.write(f"{get_args(field.annotation)=}")
                if origin is list:
                    with st.container(border=True):
                        raw_input_values[name] = _models_list_to_input_components(get_args(field.annotation)[0])
            elif isclass(field.annotation) and issubclass(field.annotation, BaseModel):
                with st.container(border=True):
                    raw_input_values[name] = _model_to_input_components(field.annotation)
            else:
                raise

    return model(**raw_input_values)


def _models_list_to_input_components(models: type[_T]) -> list[_T]:
    n_items = st.number_input("Number of items", min_value=1, value=1)
    st.write(f"{n_items=}")
    return [_model_to_input_components(models) for _ in range(n_items)]
