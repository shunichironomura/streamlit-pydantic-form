from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget

st.markdown("# Simple form example")


class SimpleFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Form slider")]
    checkbox_val: Annotated[bool, widget.Checkbox("Form checkbox")]


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


st.markdown("# Nested form example")


class ChildFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Child slider")]


class ParentFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Parent slider")]
    checkbox_val: Annotated[bool, widget.Checkbox("Parent checkbox")]
    child: ChildFormModel


with st_auto_form("form_2", model=ParentFormModel) as parent_form:
    input_values2 = parent_form.input_components()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(
            "parent slider",
            input_values2.slider_val,
            "parent checkbox",
            input_values2.checkbox_val,
            "child slider",
            input_values2.child.slider_val,
        )

st.markdown("# Custom widget example")


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


# Form model
class PointFormModel(BaseModel):
    p: Annotated[PointModel, PointWidget()]


with st_auto_form("form_3", model=PointFormModel) as point_form:
    input_values3 = point_form.input_components()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("p", input_values3.p)
