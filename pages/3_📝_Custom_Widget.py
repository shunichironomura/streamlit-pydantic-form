import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget

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
