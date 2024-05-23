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


form = DynamicForm("form_4", model=PointListModel)
form.input_widgets()
if form.submitted:
    st.write("points", form.value.points)
