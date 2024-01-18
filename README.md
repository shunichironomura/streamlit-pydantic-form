# Streamlit Pydnatic Form

Streamlit form component defined by a Pydantic model.

## Installation

```bash
pip install streamlit-pydantic-form
```

## Usage

### Without `streamlit-pydantic-form`

```python
import streamlit as st

with st.form("form_0"):
    slider_val = st.slider("Form slider")
    checkbox_val = st.checkbox("Form checkbox")

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", slider_val, "checkbox", checkbox_val)
```

### With `streamlit-pydantic-form`

With `streamlit-pydantic-form` you can define a Pydantic model and use it to automatically generate a form.

```python
from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget

class SimpleFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Form slider")]
    checkbox_val: Annotated[bool, widget.Checkbox("Form checkbox")]


with st_auto_form("form_1", model=SimpleFormModel) as simple_form:
    val = simple_form.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("slider", val.slider_val, "checkbox", val.checkbox_val)
```

### Nested Model

You can also define a nested model.

```python
from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget

class ChildFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Child slider")]

class ParentFormModel(BaseModel):
    slider_val: Annotated[int, widget.Slider("Parent slider")]
    checkbox_val: Annotated[bool, widget.Checkbox("Parent checkbox")]
    child: ChildFormModel

with st_auto_form("form_2", model=ParentFormModel) as parent_form:
    val2 = parent_form.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(
            "parent slider",
            val2.slider_val,
            "parent checkbox",
            val2.checkbox_val,
            "child slider",
            val2.child.slider_val,
        )
```

### Custom Widget

You can define a custom widget by defining a custom `WidgetBuilder` and pass it to `st_auto_form` as `widget_builder`.

```python
from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget

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
```

You can also use the `Annotated` type hint to define a custom widget.

```python
from typing import Annotated

import streamlit as st
from pydantic import BaseModel

from streamlit_pydantic_form import st_auto_form, widget

# External model
class PointModel(BaseModel):
    x: int
    y: int

# Custom widget
class PointWidget(widget.WidgetBuilder):
    def build(self) -> PointModel:
        x = st.slider("X")
        y = st.slider("Y")
        return PointModel(x=x, y=y)

# Form model
class PointFormModel(BaseModel):
    p: Annotated[PointModel, PointWidget()]

with st_auto_form("form_4", model=PointFormModel) as point_form2:
    val4 = point_form2.input_widgets()
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("x", val4.p.x, "y", val4.p.y)
```
