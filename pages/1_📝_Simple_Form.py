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
