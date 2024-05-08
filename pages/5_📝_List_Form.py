from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import static, widget

st.markdown("# Custom widget example 2")


class PointModel(BaseModel):
    x: Annotated[int, widget.Slider("X")]
    y: Annotated[int, widget.Slider("Y")]


class PointListModel(BaseModel):
    points: list[PointModel]


form = static("form_4", model=PointListModel)
val = form.input_widgets()
submitted = form.form_submit_button("Submit")
if submitted:
    st.write("points", val.points)
