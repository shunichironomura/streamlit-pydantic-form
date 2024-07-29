__all__ = [
    "StaticForm",
    "DynamicForm",
]
import warnings
from collections.abc import Callable, Generator, Sequence
from contextlib import contextmanager
from inspect import isclass
from types import GenericAlias, TracebackType
from typing import Any, Generic, Self, TypeVar, get_args, get_origin

import streamlit as st
from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from streamlit.delta_generator import DeltaGenerator
from typing_extensions import deprecated

from ._exceptions import NotYetSubmittedError, NoWidgetBuilderFoundError
from .widget import WidgetBuilder

T = TypeVar("T", bound=BaseModel)

SESSION_STATE_KEY_PREFIX = "streamlit_pydantic_form"


class StaticForm(Generic[T]):
    def __init__(
        self,
        key: str,
        *,
        model: type[T],
        clear_on_submit: bool = False,
        border: bool = True,
        widget_builder: WidgetBuilder[T] | None = None,
    ) -> None:
        self.model = model
        self.key = key
        self.form = st.form(key=self.key, clear_on_submit=clear_on_submit, border=border)
        self.widget_builder = widget_builder

    @property
    def _session_state_base_key(self) -> str:
        return f"{SESSION_STATE_KEY_PREFIX}:{self.key}"

    def input_widgets(self) -> T:
        if self.widget_builder is not None:
            return self.widget_builder.build(self.form)
        return model_to_input_components(self.model, form=self.form, base_key=self._session_state_base_key)

    @deprecated(
        "st_auto_form.input_components() is deprecated, use st_auto_form.input_widgets() instead",
    )
    def input_components(self) -> T:
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


class DynamicForm(Generic[T]):
    """A dynamic form that can be used to render input widgets for a Pydantic model."""

    def __init__(
        self,
        key: str,
        *,
        model: type[T],
        border: bool = True,
        widget_builder: WidgetBuilder[T] | None = None,
    ) -> None:
        self.key = key
        self.model = model
        self.border = border
        self.widget_builder = widget_builder

    @property
    def _session_state_key_submitted(self) -> str:
        """Key to store the submitted state of the form."""
        return f"{SESSION_STATE_KEY_PREFIX}:{self.key}:submitted"

    @property
    def _session_state_base_key(self) -> str:
        """Base key to store the form's input values."""
        return f"{SESSION_STATE_KEY_PREFIX}:{self.key}"

    @property
    def submitted(self) -> bool:
        """Whether the form has been submitted."""
        return st.session_state.get(self._session_state_key_submitted, False)

    @property
    def value(self) -> T:
        """The form's input values."""
        if not self.submitted:
            raise NotYetSubmittedError

        return restore_object_from_session_state(self._session_state_base_key, self.model)

    @contextmanager
    def on_submit(self) -> Generator[None, None, None]:
        """Context manager to run code when the form is submitted.

        It resets the submitted state to `False` after the context manager exits.
        This context manager should be used when `submitted` is `True`.
        If `submitted` is `False`, it raises a `NotYetSubmittedError`.

        Example:
        -------
        ```python
        form = DynamicForm("form", model=MyModel)
        form.input_widgets()
        if form.submitted:
            with form.on_submit():
                st.write(form.value)
        ```

        """
        if self.submitted:
            try:
                yield
            finally:
                st.session_state[self._session_state_key_submitted] = False
        else:
            raise NotYetSubmittedError

    def input_widgets(self) -> None:
        """Render the form's input widgets."""
        self._form_fragment()

    @st.fragment
    def _form_fragment(self) -> T:
        with st.container(border=self.border):
            value = model_to_input_components(
                self.model,
                value=None,
                base_key=self._session_state_base_key,
            )
            if st.button("Submit"):
                st.session_state[self._session_state_key_submitted] = True
                st.rerun()
        return value


def extract_widget_builder_from_metadata(metadata: list[Any]) -> WidgetBuilder[Any]:
    try:
        return next(item for item in metadata if isinstance(item, WidgetBuilder))
    except StopIteration as e:
        raise NoWidgetBuilderFoundError from e


def restore_object_from_session_state(base_key: str, model: type[T]) -> T:
    raw_input_values = {}

    for name, field in model.model_fields.items():
        # if the field is another model, recursively restore it
        if isclass(field.annotation) and issubclass(field.annotation, BaseModel):
            raw_input_values[name] = restore_object_from_session_state(f"{base_key}.{name}", field.annotation)
        # if the field is a list of models, recursively restore each item
        elif isinstance(field.annotation, GenericAlias) and get_origin(field.annotation) is list:
            raw_input_values[name] = [
                restore_object_from_session_state(f"{base_key}.{name}[{idx}]", get_args(field.annotation)[0])
                for idx in range(st.session_state[f"{base_key}.{name}:__n_items"])
            ]
        else:
            raw_input_values[name] = st.session_state[f"{base_key}.{name}"]

    return model(**raw_input_values)


SUPPORTED_GENERIC_ALIAS = {list}


def model_to_input_components(
    model: type[T],
    *,
    base_key: str,
    form: DeltaGenerator | None = None,
    value: T | None = None,
) -> T:
    raw_input_values = {}
    for name, field in model.model_fields.items():
        try:
            builder = extract_widget_builder_from_metadata(field.metadata)
            if value is not None:
                builder.default = getattr(value, name)
            elif field.default is not PydanticUndefined:
                builder.default = field.default
            raw_input_values[name] = builder.build(form, randomize_key=False, kwargs={"key": f"{base_key}.{name}"})

        except NoWidgetBuilderFoundError:
            if field.annotation is None:
                raise
            if (
                isinstance(field.annotation, GenericAlias)
                and (origin := get_origin(field.annotation)) in SUPPORTED_GENERIC_ALIAS
            ):
                if origin is list:
                    if form is not None:
                        msg = "List fields are not supported in static forms"
                        raise ValueError(msg) from None
                    with st.container(border=True):
                        raw_input_values[name] = models_list_to_input_components(
                            get_args(field.annotation)[0],
                            key=f"{base_key}.{name}",
                            value=getattr(value, name, None),
                        )
                else:
                    raise
            elif isclass(field.annotation) and issubclass(field.annotation, BaseModel):
                with st.container(border=True):
                    raw_input_values[name] = model_to_input_components(
                        field.annotation,
                        base_key=f"{base_key}.{name}",
                        form=form,
                        value=getattr(value, name, None),
                    )
            else:
                raise

    return model(**raw_input_values)


def models_list_to_input_components(model: type[T], *, key: str, value: Sequence[T] | None = None) -> list[T]:
    n_items = int(st.number_input(f"Number of `{model.__name__}` items", min_value=0, value=1))
    st.session_state[f"{key}:__n_items"] = n_items

    def get_default_value(value: Sequence[T] | None, idx: int) -> T | None:
        if value is None:
            return None
        try:
            return value[idx]
        except IndexError:
            return None

    return [
        model_to_input_components(
            model,
            base_key=f"{key}[{idx}]",
            value=get_default_value(value, idx),
        )
        for idx in range(n_items)
    ]
