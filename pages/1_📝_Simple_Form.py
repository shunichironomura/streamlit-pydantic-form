from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import StaticForm, widget

st.markdown("# Simple form example")


class SimpleFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Form slider")] = 10
    checkbox_val: Annotated[bool, widget.Checkbox("Form checkbox")]


with StaticForm("simple_static_form", model=SimpleFormModel) as simple_form:
    val = simple_form.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", val.slider_val, "checkbox", val.checkbox_val)
