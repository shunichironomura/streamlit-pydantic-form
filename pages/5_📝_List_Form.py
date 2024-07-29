from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import DynamicForm, widget

st.markdown("# Custom widget example 2")


class PointModel(BaseModel):
    x: Annotated[int, widget.Slider("X")]
    y: Annotated[int, widget.Slider("Y")]


class PointListModel(BaseModel):
    points: list[PointModel]


if "points" not in st.session_state:
    st.session_state.points = []


form = DynamicForm("list_form", model=PointListModel)

if st.button("Add points") and not st.button("Cancel"):
    form.input_widgets()

if form.submitted:
    with form.on_submit():
        st.write("Added points", form.value.points)
        st.session_state.points.extend(form.value.points)

st.write("All points", st.session_state.points)
