from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import StaticForm, widget

st.markdown("# Nested form example")


class ChildFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Child slider")]


class ParentFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Parent slider")]
    checkbox_val: Annotated[bool, widget.Checkbox("Parent checkbox")]
    child: ChildFormModel


with StaticForm("nested_static_form", model=ParentFormModel) as parent_form:
    val2 = parent_form.input_widgets()
    submitted = parent_form.form_submit_button("Submit")
    if submitted:
        st.write(
            "parent slider",
            val2.slider_val,
            "parent checkbox",
            val2.checkbox_val,
            "child slider",
            val2.child.slider_val,
        )
