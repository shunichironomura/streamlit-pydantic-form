from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import DynamicForm, widget

st.markdown("# Simple form example")


class SimpleFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Form slider")] = 10
    checkbox_val: Annotated[bool, widget.Checkbox("Form checkbox")]


form = DynamicForm("form_1", model=SimpleFormModel)

form.input_widgets()
if form.submitted:
    st.write("slider", form.value.slider_val, "checkbox", form.value.checkbox_val)
