import warnings
from collections.abc import Callable, Sequence
from functools import wraps
from inspect import isclass
from types import GenericAlias, TracebackType
from typing import Any, Generic, ParamSpec, Self, TypeVar, get_args, get_origin

import streamlit as st
from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from streamlit.delta_generator import DeltaGenerator
from typing_extensions import deprecated

from .widget import WidgetBuilder

_T = TypeVar("_T", bound=BaseModel)


class StaticForm(Generic[_T]):
    def __init__(
        self,
        key: str,
        *,
        model: type[_T],
        clear_on_submit: bool = False,
        border: bool = True,
        widget_builder: WidgetBuilder[_T] | None = None,
    ) -> None:
        self.model = model
        self.form = st.form(key=key, clear_on_submit=clear_on_submit, border=border)
        self.widget_builder = widget_builder

    def input_widgets(self) -> _T:
        if self.widget_builder is not None:
            return self.widget_builder.build(self.form)
        return _model_to_input_components(self.model, form=self.form)

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

    @property
    def form_submit_button(self) -> Callable[..., bool]:
        return self.form.form_submit_button

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


class NotYetSubmittedError(Exception):
    pass


class DynamicForm(Generic[_T]):
    def __init__(
        self,
        key: str,
        *,
        model: type[_T],
        border: bool = True,
        widget_builder: WidgetBuilder[_T] | None = None,
    ) -> None:
        self.key = key
        self.model = model
        self.border = border
        self.widget_builder = widget_builder

    @property
    def _session_state_key(self) -> dict[str, str]:
        return {k: f"streamlit_pydantic_dynamic_form_{self.key}_{k}" for k in ("value", "submitted")}

    @property
    def submitted(self) -> bool:
        return st.session_state.get(self._session_state_key["submitted"], False)

    @property
    def value(self) -> _T:
        if not self.submitted or self._session_state_key["value"] not in st.session_state:
            raise NotYetSubmittedError
        return st.session_state[self._session_state_key["value"]]  # type: ignore[no-any-return]

    def input_widgets(self) -> _T:
        if self.widget_builder is not None:
            return self.widget_builder.build()
        val = self._form_fragment()

        # if self.submitted:
        # val = st.session_state[self._session_state_key["value"]]

        return val

    @st.experimental_fragment
    def _form_fragment(self) -> _T:
        with st.container(border=self.border):
            current_value = st.session_state.get(self._session_state_key["value"], None)
            print(f"{current_value=}")
            value = _model_to_input_components(self.model, value=current_value)
            print(f"{value=}")
            st.session_state[self._session_state_key["value"]] = value
            if st.button("Submit"):
                st.session_state[self._session_state_key["submitted"]] = True
                st.session_state[self._session_state_key["value"]] = value
                st.rerun()
        return value


class NoWidgetBuilderFoundError(Exception):
    pass


def _extract_widget_builder_from_metadata(metadata: list[Any]) -> WidgetBuilder[Any]:
    try:
        return next(item for item in metadata if isinstance(item, WidgetBuilder))
    except StopIteration as e:
        msg = "No widget builder found in metadata"
        raise NoWidgetBuilderFoundError(msg) from e


_SUPPORTED_GENERIC_ALIAS = {list}

_P = ParamSpec("_P")
_R = TypeVar("_R")


class containerize:  # noqa: N801
    def __init__(self, *, height: int | None = None, border: bool | None = None) -> None:
        self.height = height
        self.border = border

    def __call__(self, func: Callable[_P, _R]) -> Callable[_P, _R]:
        @wraps(func)
        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            with st.container(height=self.height, border=self.border):
                return func(*args, **kwargs)

        return wrapper


def _model_to_input_components(
    model: type[_T],
    *,
    form: DeltaGenerator | None = None,
    randomize_key: bool = False,
    value: _T | None = None,
) -> _T:
    print(f"{value=}")
    raw_input_values = {}
    for name, field in model.model_fields.items():
        try:
            builder = _extract_widget_builder_from_metadata(field.metadata)
            if value is not None:
                builder.default = getattr(value, name)
                print(f"{builder.default=}")
            elif field.default is not PydanticUndefined:
                builder.default = field.default
            raw_input_values[name] = builder.build(form, randomize_key=randomize_key)
            print(f"165{raw_input_values=}")

        except NoWidgetBuilderFoundError:
            if field.annotation is None:
                raise
            if (
                isinstance(field.annotation, GenericAlias)
                and (origin := get_origin(field.annotation)) in _SUPPORTED_GENERIC_ALIAS
            ):
                if origin is list:
                    if form is not None:
                        msg = "List fields are not supported in static forms"
                        raise ValueError(msg) from None
                    with st.container(border=True):
                        raw_input_values[name] = _models_list_to_input_components(
                            get_args(field.annotation)[0],
                            value=getattr(value, name, None),
                        )
                        print(f"{raw_input_values=}")
                else:
                    raise
            elif isclass(field.annotation) and issubclass(field.annotation, BaseModel):
                with st.container(border=True):
                    raw_input_values[name] = _model_to_input_components(
                        field.annotation,
                        form=form,
                        randomize_key=randomize_key,
                        value=getattr(value, name, None),
                    )
            else:
                raise

    return model(**raw_input_values)


def _models_list_to_input_components(model: type[_T], *, value: Sequence[_T] | None = None) -> list[_T]:
    print(f"{value=}")
    n_items = int(st.number_input(f"Number of `{model.__name__}` items", min_value=1, value=1))

    def get_default_value(value: Sequence[_T] | None, idx: int) -> _T | None:
        if value is None:
            return None
        try:
            return value[idx]
        except IndexError:
            return None

    return [
        _model_to_input_components(model, randomize_key=True, value=get_default_value(value, idx))
        for idx in range(n_items)
    ]
