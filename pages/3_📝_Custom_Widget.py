import streamlit as st
from pydantic import BaseModel
from streamlit.delta_generator import DeltaGenerator

from streamlit_pydantic_form import static_form, widget

st.markdown("# Custom widget example")


# External model
class PointModel(BaseModel):
    x: int
    y: int


# Custom widget builder
class PointWidget(widget.WidgetBuilder[PointModel]):
    def build(self, form: DeltaGenerator, *, randomize_key: bool = False) -> PointModel:  # noqa: ARG002
        x = form.slider("X")
        y = form.slider("Y")
        return PointModel(x=x, y=y)


with static_form("form_3", model=PointModel, widget_builder=PointWidget()) as point_form:
    val3 = point_form.input_widgets()
    submitted = point_form.form_submit_button("Submit")
    if submitted:
        st.write("x", val3.x, "y", val3.y)
