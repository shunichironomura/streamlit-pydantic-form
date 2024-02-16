from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget

st.markdown("# Custom widget example 2")


# External model
class PointModel(BaseModel):
    x: int
    y: int


# Custom widget builder
class PointWidget(widget.WidgetBuilder[PointModel]):
    def build(self) -> PointModel:
        x = st.slider("X")
        y = st.slider("Y")
        return PointModel(x=x, y=y)


# Combination of custom and annotated widgets
class PointFormModel(BaseModel):
    p: Annotated[PointModel, PointWidget()]


with st_auto_form("form_4", model=PointFormModel) as point_form2:
    val4 = point_form2.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("x", val4.p.x, "y", val4.p.y)
