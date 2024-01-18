# Streamlit Pydnatic Form

Streamlit form component defined by a Pydantic model.

> [!WARNING]
> This is a work in progress.

## Usage

### Without `streamlit-pydantic-form`

```python
import streamlit as st

with st.form("my_form"):
    st.write("Inside the form")
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")
```

### With `streamlit-pydantic-form`

With `streamlit-pydantic-form` you can define a Pydantic model and use it to automatically generate a form.

```python
from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget


class MyFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Form slider")] = 0
    checkbox_val: Annotated[bool, widget.Checkbox("Form checkbox")] = False


with st_auto_form("my_form", model=MyFormModel) as my_form:
    st.write("Inside the form")
    input_values = my_form.input_components()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(
            "slider",
            input_values.slider_val,
            "checkbox",
            input_values.checkbox_val,
        )

st.write("Outside the form")

```
