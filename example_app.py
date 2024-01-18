from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget

st.markdown("# Simple form example")


class SimpleFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Form slider")]
    checkbox_val: Annotated[bool, widget.Checkbox("Form checkbox")]


with st_auto_form("form_1", model=SimpleFormModel) as simple_form:
    val = simple_form.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", val.slider_val, "checkbox", val.checkbox_val)


st.markdown("# Nested form example")


class ChildFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Child slider")]


class ParentFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Parent slider")]
    checkbox_val: Annotated[bool, widget.Checkbox("Parent checkbox")]
    child: ChildFormModel


with st_auto_form("form_2", model=ParentFormModel) as parent_form:
    val2 = parent_form.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(
            "parent slider",
            val2.slider_val,
            "parent checkbox",
            val2.checkbox_val,
            "child slider",
            val2.child.slider_val,
        )

st.markdown("# Custom widget example")


# External model
class PointModel(BaseModel):
    x: int
    y: int


# Custom widget builder
class PointWidget(widget.WidgetBuilder):
    def build(self) -> PointModel:
        x = st.slider("X")
        y = st.slider("Y")
        return PointModel(x=x, y=y)


with st_auto_form("form_3", model=PointModel, widget_builder=PointWidget()) as point_form:
    val3 = point_form.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("x", val3.x, "y", val3.y)

st.markdown("# Custom widget example 2")


# Combination of custom and annotated widgets
class PointFormModel(BaseModel):
    p: Annotated[PointModel, PointWidget()]


with st_auto_form("form_4", model=PointFormModel) as point_form2:
    val4 = point_form2.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("x", val4.p.x, "y", val4.p.y)
