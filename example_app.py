from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget


# One widget per field
class SimpleFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Form slider")] = 0
    checkbox_val: Annotated[bool, widget.Checkbox("Form checkbox")] = False


with st_auto_form("form_1", model=SimpleFormModel) as simple_form:
    input_values = simple_form.input_components()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(
            "slider",
            input_values.slider_val,
            "checkbox",
            input_values.checkbox_val,
        )


# External model
class PointModel(BaseModel):
    x: int
    y: int


# Custom widget
class PointWidget(widget.WidgetBuilder):
    def build(self) -> PointModel:
        x = st.slider("X")
        y = st.slider("Y")
        return PointModel(x=x, y=y)


# Nested model
class PointFormModel(BaseModel):
    p: Annotated[PointModel, PointWidget()]
    q: SimpleFormModel


with st_auto_form("form_2", model=PointFormModel) as point_form:
    input_values2 = point_form.input_components()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("p", input_values2.p, "q", input_values2.q)
