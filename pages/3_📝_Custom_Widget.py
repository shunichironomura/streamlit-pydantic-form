from typing import Any

import streamlit as st
from pydantic import BaseModel
from streamlit.delta_generator import DeltaGenerator

from streamlit_pydantic_form import StaticForm, widget

st.markdown("# Custom widget example")


# External model
class PointModel(BaseModel):
    x: int
    y: int


# Custom widget builder
class PointWidget(widget.WidgetBuilder[PointModel]):
    def build(
        self,
        form: DeltaGenerator | None = None,
        *,
        randomize_key: bool = False,  # noqa: ARG002
        value: PointModel | None = None,  # noqa: ARG002
        kwargs: dict[str, Any] | None = None,  # noqa: ARG002
    ) -> PointModel:
        assert form is not None
        x = form.slider("X")
        y = form.slider("Y")
        return PointModel(x=x, y=y)


with StaticForm("custom_widget_form", model=PointModel, widget_builder=PointWidget()) as point_form:
    val3 = point_form.input_widgets()
    submitted = point_form.form_submit_button("Submit")
    if submitted:
        st.write("x", val3.x, "y", val3.y)
